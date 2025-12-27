from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.system import router as system_router
from app.api.health import router as health_router
from app.api.docker import router as docker_router

app = FastAPI(title="Homebox Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # On sécurisera plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(system_router, prefix="/api")
app.include_router(docker_router, prefix="/api")

