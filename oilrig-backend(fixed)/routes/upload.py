from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from openpyxl import load_workbook
from tempfile import NamedTemporaryFile
from db import get_db_pool
from datetime import date
from collections import defaultdict

router = APIRouter(prefix="/api/upload", tags=["Excel Upload"])

@router.post("/excel")
async def upload_excel(file: UploadFile = File(...), oilrig_id: int = Query(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")

    try:
        temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
        contents = await file.read()
        temp_file.write(contents)
        temp_file.close()

        workbook = load_workbook(temp_file.name, data_only=True)
        sheet = workbook.active

        pool = get_db_pool()
        async with pool.acquire() as conn:
            templates = await conn.fetch("SELECT * FROM Templates")
            checks = await conn.fetch("SELECT * FROM Template_checks")

            check_map = defaultdict(list)
            for c in checks:
                check_map[c["template_id"]].append(c)

            matched_template = None
            for template in templates:
                template_id = template["id"]
                passed = True
                for check in check_map[template_id]:
                    cell = check["check_cell"]
                    expected = check["check_value"]
                    actual = sheet[cell].value
                    if actual is None or str(actual).strip() != expected.strip():
                        passed = False
                        break

                if passed:
                    matched_template = template
                    break

            if not matched_template:
                raise HTTPException(status_code=400, detail="No matching template found")

            data_locations = await conn.fetch("SELECT * FROM Data_locations WHERE template_id = $1", matched_template["id"])
            today = date.today()
            extracted_values = []

            for loc in data_locations:
                cell = loc["data_cell"]
                try:
                    raw_value = sheet[cell].value
                    value = float(raw_value) if raw_value is not None else None
                except Exception:
                    value = None

                if value is not None:
                    extracted_values.append({
                        "report_type": loc["report_type"],
                        "resource_type": loc["resource_type"],
                        "data_type": loc["data_type"],
                        "value": value
                    })

            if not extracted_values:
                raise HTTPException(status_code=400, detail="No values found in Excel")

            inserted_report_ids = {}

            for entry in extracted_values:
                r_type = entry["report_type"]
                r_date = today.replace(day=1) if r_type == 'monthly' else \
                         today.replace(month=1, day=1) if r_type == 'annually' else today

                key = (r_type, r_date)
                if key not in inserted_report_ids:
                    report_id = await conn.fetchval("""
                        INSERT INTO Reports (oilrig_id, report_type, report_date)
                        VALUES ($1, $2::report_type_enum, $3)
                        ON CONFLICT (oilrig_id, report_type, report_date)
                        DO UPDATE SET updated_at = NOW()
                        RETURNING id
                    """, oilrig_id, r_type, r_date)
                    inserted_report_ids[key] = report_id

                await conn.execute("""
                    INSERT INTO Report_data (report_id, resource_type, data_type, value)
                    VALUES ($1, $2::resource_type_enum, $3::data_type_enum, $4)
                    ON CONFLICT (report_id, resource_type, data_type)
                    DO UPDATE SET value = $4, updated_at = NOW()
                """, inserted_report_ids[key], entry["resource_type"], entry["data_type"], entry["value"])

            return {
                "status": "uploaded",
                "oilrig_id": oilrig_id,
                "report_date": str(today),
                "matched_template": matched_template["temp_name"],
                "values_saved": extracted_values
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
