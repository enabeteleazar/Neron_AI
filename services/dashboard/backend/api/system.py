import psutil
from fastapi import APIRouter

router = APIRouter()

@router.get("/system")
def system_status():
    return {
        "cpu": {
            "percent": psutil.cpu_percent(interval=0.5)
        },
        "ram": {
            "total": psutil.virtual_memory().total,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent
        }
    }
