from fastapi import APIRouter
from app.database.connection import get_connection

router = APIRouter(tags=["Database"])


@router.get("/database")
def database_check():
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT version();")

    version = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "status": "connected",
        "postgres": version
    }

