from fastapi import APIRouter, Query
from db import get_db_pool
from datetime import datetime

router = APIRouter(prefix="/api/reports", tags=["Reports"])

# 1. Daily report of all rigs by date
@router.get("/daily")
async def get_daily_report(date: str = Query(..., description="YYYY-MM-DD")):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT o.name, r.report_date, d.value AS real_oil
            FROM Reports r
            JOIN Report_data d ON r.id = d.report_id
              AND d.resource_type = 'oil'::resource_type_enum
              AND d.data_type = 'real'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'daily'::report_type_enum
              AND r.report_date = $1
        """
        records = await conn.fetch(query, parsed_date)
        return [dict(record) for record in records]

# 2. Daily report by rig name
@router.get("/daily/by-rig")
async def get_daily_by_rig(name: str = Query(...)):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT o.name, r.report_date, d.value AS real_oil
            FROM Reports r
            JOIN Report_data d ON r.id = d.report_id
              AND d.resource_type = 'oil'::resource_type_enum
              AND d.data_type = 'real'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'daily'::report_type_enum
              AND o.name = $1
            ORDER BY r.report_date DESC
        """
        records = await conn.fetch(query, name)
        return [dict(row) for row in records]

# 3. Weekly actual oil and gas
@router.get("/daily/weekly")
async def get_weekly_real(start_date: str, end_date: str):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}

    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT o.name, r.report_date,
                   oil_real.value AS real_oil,
                   gas_real.value AS real_gas
            FROM Reports r
            LEFT JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            LEFT JOIN Report_data gas_real ON r.id = gas_real.report_id
              AND gas_real.resource_type = 'gas'::resource_type_enum
              AND gas_real.data_type = 'real'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'daily'::report_type_enum
              AND r.report_date BETWEEN $1 AND $2
            ORDER BY r.report_date
        """
        records = await conn.fetch(query, start, end)
        return [dict(r) for r in records]

# 4. Monthly planned & real
@router.get("/monthly")
async def get_monthly(year: int, month: int):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT o.name, r.report_date,
                   oil_planned.value AS planned_oil,
                   gas_planned.value AS planned_gas,
                   oil_real.value AS real_oil,
                   gas_real.value AS real_gas
            FROM Reports r
            LEFT JOIN Report_data oil_planned ON r.id = oil_planned.report_id
              AND oil_planned.resource_type = 'oil'::resource_type_enum
              AND oil_planned.data_type = 'planned'::data_type_enum
            LEFT JOIN Report_data gas_planned ON r.id = gas_planned.report_id
              AND gas_planned.resource_type = 'gas'::resource_type_enum
              AND gas_planned.data_type = 'planned'::data_type_enum
            LEFT JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            LEFT JOIN Report_data gas_real ON r.id = gas_real.report_id
              AND gas_real.resource_type = 'gas'::resource_type_enum
              AND gas_real.data_type = 'real'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'monthly'::report_type_enum
              AND EXTRACT(YEAR FROM r.report_date) = $1
              AND EXTRACT(MONTH FROM r.report_date) = $2
            ORDER BY r.report_date
        """
        records = await conn.fetch(query, year, month)
        return [dict(row) for row in records]

# 5. Quarterly (3-month range)
@router.get("/quarterly")
async def get_quarter(start_month: str, end_month: str):
    try:
        start = datetime.strptime(start_month, "%Y-%m-%d").date()
        end = datetime.strptime(end_month, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-01"}

    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT o.name, r.report_date,
                   oil_planned.value AS planned_oil,
                   gas_planned.value AS planned_gas,
                   oil_real.value AS real_oil,
                   gas_real.value AS real_gas
            FROM Reports r
            LEFT JOIN Report_data oil_planned ON r.id = oil_planned.report_id
              AND oil_planned.resource_type = 'oil'::resource_type_enum
              AND oil_planned.data_type = 'planned'::data_type_enum
            LEFT JOIN Report_data gas_planned ON r.id = gas_planned.report_id
              AND gas_planned.resource_type = 'gas'::resource_type_enum
              AND gas_planned.data_type = 'planned'::data_type_enum
            LEFT JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            LEFT JOIN Report_data gas_real ON r.id = gas_real.report_id
              AND gas_real.resource_type = 'gas'::resource_type_enum
              AND gas_real.data_type = 'real'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'monthly'::report_type_enum
              AND r.report_date BETWEEN $1 AND $2
            ORDER BY r.report_date
        """
        records = await conn.fetch(query, start, end)
        return [dict(row) for row in records]
    
@router.get("/annually")
async def get_annually(year: int):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT o.name, r.report_date,
                   oil_planned.value AS planned_oil,
                   gas_planned.value AS planned_gas,
                   oil_real.value AS real_oil,
                   gas_real.value AS real_gas
            FROM Reports r
            LEFT JOIN Report_data oil_planned ON r.id = oil_planned.report_id
              AND oil_planned.resource_type = 'oil'::resource_type_enum
              AND oil_planned.data_type = 'planned'::data_type_enum
            LEFT JOIN Report_data gas_planned ON r.id = gas_planned.report_id
              AND gas_planned.resource_type = 'gas'::resource_type_enum
              AND gas_planned.data_type = 'planned'::data_type_enum
            LEFT JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            LEFT JOIN Report_data gas_real ON r.id = gas_real.report_id
              AND gas_real.resource_type = 'gas'::resource_type_enum
              AND gas_real.data_type = 'real'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'annually'::report_type_enum
              AND EXTRACT(YEAR FROM r.report_date) = $1
            ORDER BY r.report_date
        """
        records = await conn.fetch(query, year)
        return [dict(row) for row in records]

# 7. Daily vs Monthly Planned Percentage
@router.get("/percent/daily")
async def get_daily_percentage(date: str):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}

    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT r.report_date, o.name,
                   oil_real.value AS real_oil,
                   oil_planned.value AS planned_oil,
                   (oil_real.value / NULLIF(oil_planned.value, 0)) * 100 AS oil_production_percentage
            FROM Reports r
            JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            JOIN Reports rm ON r.oilrig_id = rm.oilrig_id
              AND rm.report_type = 'monthly'::report_type_enum
              AND EXTRACT(YEAR FROM r.report_date) = EXTRACT(YEAR FROM rm.report_date)
              AND EXTRACT(MONTH FROM r.report_date) = EXTRACT(MONTH FROM rm.report_date)
            JOIN Report_data oil_planned ON rm.id = oil_planned.report_id
              AND oil_planned.resource_type = 'oil'::resource_type_enum
              AND oil_planned.data_type = 'planned'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'daily'::report_type_enum
              AND r.report_date = $1
        """
        records = await conn.fetch(query, parsed_date)
        return [dict(row) for row in records]

# 8. Monthly Real Oil vs Planned Oil (same month)
@router.get("/percent/monthly")
async def get_monthly_percentage(year: int, month: int):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT r.report_date, o.name,
                   oil_real.value AS real_oil,
                   oil_planned.value AS planned_oil,
                   (oil_real.value / NULLIF(oil_planned.value, 0)) * 100 AS oil_production_percentage
            FROM Reports r
            JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            JOIN Report_data oil_planned ON r.id = oil_planned.report_id
              AND oil_planned.resource_type = 'oil'::resource_type_enum
              AND oil_planned.data_type = 'planned'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'monthly'::report_type_enum
              AND EXTRACT(YEAR FROM r.report_date) = $1
              AND EXTRACT(MONTH FROM r.report_date) = $2
            ORDER BY r.report_date;
        """
        records = await conn.fetch(query, year, month)
        return [dict(row) for row in records]

# 9. Monthly Real vs Annual Planned
@router.get("/percent/monthly-vs-annual")
async def get_monthly_vs_annual_percentage(year: int, month: int):
    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT r.report_date, o.name,
                   oil_real.value AS real_oil,
                   oil_planned.value AS planned_annual_oil,
                   (oil_real.value / NULLIF(oil_planned.value, 0)) * 100 AS oil_production_percentage
            FROM Reports r
            JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            JOIN Reports ra ON r.oilrig_id = ra.oilrig_id
              AND ra.report_type = 'annually'::report_type_enum
              AND EXTRACT(YEAR FROM r.report_date) = EXTRACT(YEAR FROM ra.report_date)
            JOIN Report_data oil_planned ON ra.id = oil_planned.report_id
              AND oil_planned.resource_type = 'oil'::resource_type_enum
              AND oil_planned.data_type = 'planned'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'monthly'::report_type_enum
              AND EXTRACT(YEAR FROM r.report_date) = $1
              AND EXTRACT(MONTH FROM r.report_date) = $2
            ORDER BY r.report_date;
        """
        records = await conn.fetch(query, year, month)
        return [dict(row) for row in records]

# 10. Yearly Total Real Oil vs Annual Planned Oil
@router.get("/percent/yearly-total")
async def get_yearly_total_vs_annual(start_month: str, end_month: str):
    try:
        start = datetime.strptime(start_month, "%Y-%m-%d").date()
        end = datetime.strptime(end_month, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-01"}

    pool = get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT
                EXTRACT(YEAR FROM r.report_date) AS year,
                o.name,
                SUM(oil_real.value) AS total_real_oil,
                oil_planned.value AS planned_annual_oil,
                (SUM(oil_real.value) / NULLIF(oil_planned.value, 0)) * 100 AS oil_production_percentage
            FROM Reports r
            JOIN Report_data oil_real ON r.id = oil_real.report_id
              AND oil_real.resource_type = 'oil'::resource_type_enum
              AND oil_real.data_type = 'real'::data_type_enum
            JOIN Reports ra ON r.oilrig_id = ra.oilrig_id
              AND ra.report_type = 'annually'::report_type_enum
              AND EXTRACT(YEAR FROM r.report_date) = EXTRACT(YEAR FROM ra.report_date)
            JOIN Report_data oil_planned ON ra.id = oil_planned.report_id
              AND oil_planned.resource_type = 'oil'::resource_type_enum
              AND oil_planned.data_type = 'planned'::data_type_enum
            JOIN Oilrig o ON r.oilrig_id = o.id
            WHERE r.report_type = 'monthly'::report_type_enum
              AND r.report_date BETWEEN $1 AND $2
            GROUP BY EXTRACT(YEAR FROM r.report_date), o.name, oil_planned.value
            ORDER BY EXTRACT(YEAR FROM r.report_date);
        """
        records = await conn.fetch(query, start, end)
        return [dict(row) for row in records]
