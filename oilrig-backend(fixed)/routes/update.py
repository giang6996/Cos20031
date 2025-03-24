from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from db import get_db_pool
from asyncpg import Record
from datetime import date

router = APIRouter(prefix="/api/update", tags=["Update"])

class ReportDataUpdate(BaseModel):
    value: float

@router.put("/report-data/{report_data_id}")
async def update_report_data(
    report_data_id: int = Path(...),
    data: ReportDataUpdate = ...
):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        original: Record = await conn.fetchrow("""
            SELECT rd.*, r.report_type, r.report_date, r.oilrig_id
            FROM Report_data rd
            JOIN Reports r ON rd.report_id = r.id
            WHERE rd.id = $1
        """, report_data_id)

        if not original:
            raise HTTPException(status_code=404, detail="Report data not found")

        await conn.execute("""
            UPDATE Report_data
            SET value = $1, updated_at = NOW()
            WHERE id = $2
        """, data.value, report_data_id)

        return {"status": "updated", "id": report_data_id}
