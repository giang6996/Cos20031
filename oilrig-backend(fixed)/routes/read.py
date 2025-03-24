from fastapi import APIRouter
from db import get_db_pool

router = APIRouter(prefix="/api/read", tags=["Read"])

# Read all oilrigs
@router.get("/oilrigs")
async def get_all_oilrigs():
    pool = get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM Oilrig ORDER BY id")
        return [dict(row) for row in rows]

# Read all templates
@router.get("/templates")
async def get_all_templates():
    pool = get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM Templates ORDER BY id")
        return [dict(row) for row in rows]

# Read template checks
@router.get("/template-checks")
async def get_template_checks():
    pool = get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM Template_checks ORDER BY template_id")
        return [dict(row) for row in rows]

# Read data locations
@router.get("/data-locations")
async def get_data_locations():
    pool = get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM Data_locations ORDER BY template_id")
        return [dict(row) for row in rows]

# Read templates with checks combined
@router.get("/templates-with-checks")
async def get_templates_with_checks():
    pool = get_db_pool()
    async with pool.acquire() as conn:
        templates = await conn.fetch("SELECT * FROM Templates")
        checks = await conn.fetch("SELECT * FROM Template_checks")

        grouped = {}
        for template in templates:
            grouped[template["id"]] = {
                "id": template["id"],
                "temp_name": template["temp_name"],
                "checks": []
            }

        for check in checks:
            grouped[check["template_id"]]["checks"].append({
                "id": check["id"],
                "check_cell": check["check_cell"],
                "check_value": check["check_value"]
            })

        return list(grouped.values())