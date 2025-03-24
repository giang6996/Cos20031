from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_db_pool

router = APIRouter(prefix="/api/create", tags=["Create"])

class OilrigCreate(BaseModel):
    name: str
    report_email: str
    latitude: float
    longitude: float
    template_ids: list[int] = []

@router.post("/oilrig")
async def create_oilrig(data: OilrigCreate):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                oilrig_id = await conn.fetchval("""
                    INSERT INTO Oilrig (name, report_email, latitude, longitude)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                """, data.name, data.report_email, data.latitude, data.longitude)

                for template_id in data.template_ids:
                    await conn.execute("""
                        INSERT INTO Oilrig_templates (oilrig_id, template_id)
                        VALUES ($1, $2)
                    """, oilrig_id, template_id)

                return {"id": oilrig_id, "status": "created"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create oilrig: {str(e)}")

class TemplateCreate(BaseModel):
    temp_name: str
    checks: list[dict]  # expects { check_cell: str, check_value: str }
    data_cells: list[dict]  # expects { data_cell: str, report_type: str, resource_type: str, data_type: str }

@router.post("/template")
async def create_template(data: TemplateCreate):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        try:
            async with conn.transaction():
                template_id = await conn.fetchval("""
                    INSERT INTO Templates (temp_name)
                    VALUES ($1)
                    RETURNING id
                """, data.temp_name)

                for check in data.checks:
                    await conn.execute("""
                        INSERT INTO Template_checks (template_id, check_cell, check_value)
                        VALUES ($1, $2, $3)
                    """, template_id, check['check_cell'], check['check_value'])

                for item in data.data_cells:
                    await conn.execute("""
                        INSERT INTO Data_locations (template_id, data_cell, report_type, resource_type, data_type)
                        VALUES ($1, $2, $3::report_type_enum, $4::resource_type_enum, $5::data_type_enum)
                    """, template_id, item['data_cell'], item['report_type'], item['resource_type'], item['data_type'])

                return {"id": template_id, "status": "created"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create template: {str(e)}")
