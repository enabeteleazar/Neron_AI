#!/bin/bash

# Couleurs

RED=’\033[0;31m’
GREEN=’\033[0;32m’
YELLOW=’\033[1;33m’
BLUE=’\033[0;34m’
NC=’\033[0m’ # No Color

echo -e “${BLUE}”
echo “==========================================”
echo “  🚀 SETUP DASHBOARD SERVICE COMPLET”
echo “==========================================”
echo -e “${NC}”

# Vérifier qu’on est dans le bon répertoire

if [ ! -d “services” ]; then
echo -e “${YELLOW}⚠️  Création du répertoire services…${NC}”
mkdir -p services
fi

cd services

# Supprimer l’ancien dashboard s’il existe

if [ -d “dashboard” ]; then
echo -e “${YELLOW}⚠️  Sauvegarde de l’ancien dashboard…${NC}”
mv dashboard dashboard_backup_$(date +%Y%m%d_%H%M%S)
fi

# Créer la structure

echo -e “${GREEN}📁 Création de la structure des répertoires…${NC}”
mkdir -p dashboard/app/api

# ==========================================

# 1. main.py

# ==========================================

echo -e “${GREEN}📝 Création de main.py…${NC}”
cat > dashboard/main.py << ‘MAINPY’
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

# Configuration du logging

logging.basicConfig(
level=logging.INFO,
format=’%(asctime)s - %(name)s - %(levelname)s - %(message)s’,
handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(**name**)

app = FastAPI(
title=“Homebox Dashboard API”,
version=“1.0.0”,
description=“API pour le monitoring système et Docker”
)

# Configuration CORS

app.add_middleware(
CORSMiddleware,
allow_origins=[”*”],  # En production: remplacer par l’URL frontend
allow_credentials=True,
allow_methods=[”*”],
allow_headers=[”*”],
)

# Import des routers avec gestion d’erreur

try:
from app.api.health import router as health_router
app.include_router(health_router, prefix=”/api”, tags=[“Health”])
logger.info(“✅ Health router chargé”)
except Exception as e:
logger.error(f”❌ Erreur chargement health router: {e}”)

try:
from app.api.system import router as system_router
app.include_router(system_router, prefix=”/api”, tags=[“System”])
logger.info(“✅ System router chargé”)
except Exception as e:
logger.error(f”❌ Erreur chargement system router: {e}”)

try:
from app.api.docker import router as docker_router
app.include_router(docker_router, prefix=”/api”, tags=[“Docker”])
logger.info(“✅ Docker router chargé”)
except Exception as e:
logger.error(f”❌ Erreur chargement docker router: {e}”)

@app.on_event(“startup”)
async def startup_event():
logger.info(“🚀 Démarrage de l’API Dashboard”)

@app.on_event(“shutdown”)
async def shutdown_event():
logger.info(“🛑 Arrêt de l’API Dashboard”)

@app.get(”/”)
def root():
return {
“service”: “Homebox Dashboard API”,
“status”: “running”,
“version”: “1.0.0”
}

if **name** == “**main**”:
import uvicorn
uvicorn.run(
“main:app”,
host=“0.0.0.0”,
port=8000,
reload=False,
log_level=“info”
)
MAINPY

# ==========================================

# 2. requirements.txt

# ==========================================

echo -e “${GREEN}📝 Création de requirements.txt…${NC}”
cat > dashboard/requirements.txt << ‘REQUIREMENTS’
fastapi==0.109.0
uvicorn[standard]==0.27.0
psutil==5.9.8
docker==7.0.0
python-dotenv==1.0.0
REQUIREMENTS

# ==========================================

# 3. Dockerfile

# ==========================================

echo -e “${GREEN}📝 Création de Dockerfile…${NC}”
cat > dashboard/Dockerfile << ‘DOCKERFILE’
FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système

RUN apt-get update && apt-get install -y   
gcc   
curl   
&& rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python

COPY requirements.txt .
RUN pip install –no-cache-dir –upgrade pip &&   
pip install –no-cache-dir -r requirements.txt

# Copie du code

COPY . .

# Variables d’environnement

ENV PYTHONUNBUFFERED=1   
PYTHONDONTWRITEBYTECODE=1   
HOST=0.0.0.0   
PORT=8000

# Health check

HEALTHCHECK –interval=30s –timeout=5s –start-period=10s –retries=3   
CMD curl -f http://localhost:8000/api/health || exit 1

# Port

EXPOSE 8000

# Commande de démarrage

CMD [“uvicorn”, “main:app”, “–host”, “0.0.0.0”, “–port”, “8000”, “–log-level”, “info”]
DOCKERFILE

# ==========================================

# 4. app/**init**.py

# ==========================================

echo -e “${GREEN}📝 Création de app/**init**.py…${NC}”
cat > dashboard/app/**init**.py << ‘APPINIT’

# Fichier vide pour marquer app comme un package Python

APPINIT

# ==========================================

# 5. app/api/**init**.py

# ==========================================

echo -e “${GREEN}📝 Création de app/api/**init**.py…${NC}”
cat > dashboard/app/api/**init**.py << ‘APIINIT’

# Fichier vide pour marquer app/api comme un package Python

APIINIT

# ==========================================

# 6. app/api/health.py

# ==========================================

echo -e “${GREEN}📝 Création de app/api/health.py…${NC}”
cat > dashboard/app/api/health.py << ‘HEALTHPY’
from fastapi import APIRouter
from datetime import datetime
import logging

logger = logging.getLogger(**name**)
router = APIRouter()

@router.get(”/health”)
def health_check():
“”“Endpoint de health check”””
try:
return {
“status”: “healthy”,
“service”: “dashboard-backend”,
“timestamp”: datetime.now().isoformat()
}
except Exception as e:
logger.error(f”Erreur health check: {e}”)
return {
“status”: “unhealthy”,
“error”: str(e)
}
HEALTHPY

# ==========================================

# 7. app/api/system.py

# ==========================================

echo -e “${GREEN}📝 Création de app/api/system.py…${NC}”
cat > dashboard/app/api/system.py << ‘SYSTEMPY’
from fastapi import APIRouter, HTTPException
import psutil
from datetime import datetime
import logging

logger = logging.getLogger(**name**)
router = APIRouter()

@router.get(”/system”)
def system_status():
“”“Récupère les statistiques système”””
try:
# CPU
cpu = psutil.cpu_percent(interval=1)

```
    # RAM
    ram = psutil.virtual_memory().percent
    
    # Disque
    disk = psutil.disk_usage("/").percent
    
    # Température (avec fallback)
    temp = None
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            if 'coretemp' in temps:
                temp = temps['coretemp'][0].current
            elif 'cpu_thermal' in temps:
                temp = temps['cpu_thermal'][0].current
            else:
                # Prendre le premier capteur disponible
                first_sensor = list(temps.values())[0]
                if first_sensor:
                    temp = first_sensor[0].current
    except (AttributeError, KeyError, IndexError) as e:
        logger.debug(f"Température non disponible: {e}")
        temp = None
    
    result = {
        "cpu_percent": round(cpu, 1),
        "ram_percent": round(ram, 1),
        "disk_percent": round(disk, 1),
        "temp": round(temp, 1) if temp else 36.0,
        "status": "up",
        "timestamp": datetime.now().isoformat()
    }
    
    logger.debug(f"System: CPU={cpu}% RAM={ram}% DISK={disk}%")
    return result
    
except Exception as e:
    logger.error(f"Erreur system_status: {e}", exc_info=True)
    raise HTTPException(
        status_code=500,
        detail=f"Erreur lors de la récupération des données système: {str(e)}"
    )
```

SYSTEMPY

# ==========================================

# 8. app/api/docker.py

# ==========================================

echo -e “${GREEN}📝 Création de app/api/docker.py…${NC}”
cat > dashboard/app/api/docker.py << ‘DOCKERPY’
from fastapi import APIRouter, HTTPException
import docker
from datetime import datetime
import logging

logger = logging.getLogger(**name**)
router = APIRouter()

# Initialisation du client Docker avec gestion d’erreur

_docker_client = None

def get_docker_client():
“”“Récupère le client Docker (lazy loading)”””
global _docker_client
if _docker_client is None:
try:
_docker_client = docker.DockerClient(base_url=‘unix://var/run/docker.sock’)
_docker_client.ping()
logger.info(“✅ Docker client initialisé”)
except docker.errors.DockerException as e:
logger.error(f”❌ Erreur Docker: {e}”)
raise HTTPException(
status_code=503,
detail=“Docker n’est pas accessible. Vérifiez que le socket Docker est monté.”
)
except Exception as e:
logger.error(f”❌ Erreur inattendue Docker: {e}”)
raise HTTPException(status_code=500, detail=str(e))
return _docker_client

@router.get(”/docker”)
def docker_containers():
“”“Liste tous les conteneurs Docker”””
try:
client = get_docker_client()
containers = client.containers.list(all=True)
result = []

```
    for c in containers:
        try:
            # Calculer l'uptime
            started_at = c.attrs['State'].get('StartedAt', '')
            uptime = ""
            
            if started_at and c.status == "running":
                try:
                    start_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
                    uptime_delta = datetime.now(start_time.tzinfo) - start_time
                    days = uptime_delta.days
                    hours = uptime_delta.seconds // 3600
                    minutes = (uptime_delta.seconds % 3600) // 60
                    
                    if days > 0:
                        uptime = f"{days}j {hours}h"
                    elif hours > 0:
                        uptime = f"{hours}h {minutes}m"
                    else:
                        uptime = f"{minutes}m"
                except Exception as e:
                    logger.debug(f"Erreur calcul uptime pour {c.name}: {e}")
                    uptime = "N/A"
            
            # Récupérer les ports
            ports = []
            port_bindings = c.attrs.get('NetworkSettings', {}).get('Ports', {})
            if port_bindings:
                for container_port, host_bindings in port_bindings.items():
                    if host_bindings:
                        for binding in host_bindings:
                            host_port = binding.get('HostPort', '')
                            if host_port:
                                ports.append(host_port)
            
            # Déterminer le statut
            status = "up" if c.status == "running" else "down"
            if c.status == "paused":
                status = "warning"
            
            # Image
            image_name = "unknown"
            if c.image.tags:
                image_name = c.image.tags[0]
            else:
                image_name = c.image.short_id
            
            result.append({
                "name": c.name,
                "status": status,
                "raw_status": c.status,
                "uptime": uptime,
                "port": ports[0] if ports else "N/A",
                "image": image_name,
                "id": c.short_id
            })
            
        except Exception as e:
            logger.error(f"Erreur traitement container {c.name}: {e}")
            continue
    
    # Trier par statut (running en premier)
    result.sort(key=lambda x: (x['status'] != 'up', x['name']))
    
    logger.debug(f"Docker: {len(result)} conteneurs trouvés")
    return result
    
except HTTPException:
    raise
except docker.errors.APIError as e:
    logger.error(f"Erreur API Docker: {e}")
    raise HTTPException(status_code=500, detail=f"Erreur Docker API: {str(e)}")
except Exception as e:
    logger.error(f"Erreur docker_containers: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail=str(e))
```

@router.post(”/docker/{container_name}/start”)
def start_container(container_name: str):
“”“Démarre un conteneur”””
try:
client = get_docker_client()
container = client.containers.get(container_name)

```
    if container.status == "running":
        return {
            "success": True,
            "message": f"Container {container_name} est déjà démarré"
        }
    
    container.start()
    logger.info(f"✅ Container {container_name} démarré")
    return {
        "success": True,
        "message": f"Container {container_name} démarré avec succès"
    }
    
except docker.errors.NotFound:
    logger.error(f"Container {container_name} non trouvé")
    raise HTTPException(
        status_code=404,
        detail=f"Container {container_name} non trouvé"
    )
except docker.errors.APIError as e:
    logger.error(f"Erreur démarrage {container_name}: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

@router.post(”/docker/{container_name}/stop”)
def stop_container(container_name: str):
“”“Arrête un conteneur”””
try:
client = get_docker_client()
container = client.containers.get(container_name)

```
    if container.status != "running":
        return {
            "success": True,
            "message": f"Container {container_name} est déjà arrêté"
        }
    
    container.stop(timeout=10)
    logger.info(f"🛑 Container {container_name} arrêté")
    return {
        "success": True,
        "message": f"Container {container_name} arrêté avec succès"
    }
    
except docker.errors.NotFound:
    logger.error(f"Container {container_name} non trouvé")
    raise HTTPException(
        status_code=404,
        detail=f"Container {container_name} non trouvé"
    )
except docker.errors.APIError as e:
    logger.error(f"Erreur arrêt {container_name}: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

@router.post(”/docker/{container_name}/restart”)
def restart_container(container_name: str):
“”“Redémarre un conteneur”””
try:
client = get_docker_client()
container = client.containers.get(container_name)
container.restart(timeout=10)
logger.info(f”🔄 Container {container_name} redémarré”)
return {
“success”: True,
“message”: f”Container {container_name} redémarré avec succès”
}

```
except docker.errors.NotFound:
    logger.error(f"Container {container_name} non trouvé")
    raise HTTPException(
        status_code=404,
        detail=f"Container {container_name} non trouvé"
    )
except docker.errors.APIError as e:
    logger.error(f"Erreur redémarrage {container_name}: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

DOCKERPY

# ==========================================

# 9. .dockerignore

# ==========================================

echo -e “${GREEN}📝 Création de .dockerignore…${NC}”
cat > dashboard/.dockerignore << ‘DOCKERIGNORE’
**pycache**
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.git
.gitignore
.env
.venv
venv/
ENV/
*.log
.DS_Store
DOCKERIGNORE

# ==========================================

# 10. .gitignore

# ==========================================

echo -e “${GREEN}📝 Création de .gitignore…${NC}”
cat > dashboard/.gitignore << ‘GITIGNORE’

# Python

**pycache**/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# IDE

.vscode/
.idea/
*.swp
*.swo

# Logs

*.log

# OS

.DS_Store
Thumbs.db

# Environment

.env
.env.local
GITIGNORE

# ==========================================

# 11. README.md

# ==========================================

echo -e “${GREEN}📝 Création de README.md…${NC}”
cat > dashboard/README.md << ‘README’

# Dashboard Service

Service de monitoring système et Docker pour Homebox.

## 🚀 Démarrage rapide

### Avec Docker Compose

```bash
docker-compose up -d dashboard-backend
```

### En local (développement)

```bash
pip install -r requirements.txt
python main.py
```

## 📡 Endpoints

- `GET /` - Info service
- `GET /api/health` - Health check
- `GET /api/system` - Statistiques système (CPU, RAM, Disque, Température)
- `GET /api/docker` - Liste des conteneurs Docker
- `POST /api/docker/{name}/start` - Démarrer un conteneur
- `POST /api/docker/{name}/stop` - Arrêter un conteneur
- `POST /api/docker/{name}/restart` - Redémarrer un conteneur

## 🧪 Tests

```bash
# Health check
curl http://localhost:8000/api/health

# Système
curl http://localhost:8000/api/system

# Docker
curl http://localhost:8000/api/docker
```

## 📋 Requirements

- Python 3.11+
- Docker (pour le monitoring des conteneurs)
- Accès au socket Docker (`/var/run/docker.sock`)

## 🔧 Configuration

Variables d’environnement (optionnelles) :

- `PORT` - Port du service (défaut: 8000)
- `HOST` - Host d’écoute (défaut: 0.0.0.0)

## 📝 Logs

Les logs sont affichés sur stdout avec des émojis pour faciliter le suivi :

- ✅ = Succès
- ❌ = Erreur
- ⚠️ = Avertissement
- 🚀 = Démarrage
- 🛑 = Arrêt
  README

# ==========================================

# 12. Script de test

# ==========================================

echo -e “${GREEN}📝 Création de test_api.sh…${NC}”
cat > dashboard/test_api.sh << ‘TESTAPI’
#!/bin/bash

API_URL=”${1:-http://localhost:8000}”

echo “🧪 Test de l’API Dashboard sur $API_URL”
echo “”

# Test 1: Root

echo “1️⃣ Test de /”
curl -s “$API_URL/” | python3 -m json.tool
echo “”

# Test 2: Health

echo “2️⃣ Test de /api/health”
curl -s “$API_URL/api/health” | python3 -m json.tool
echo “”

# Test 3: System

echo “3️⃣ Test de /api/system”
curl -s “$API_URL/api/system” | python3 -m json.tool
echo “”

# Test 4: Docker

echo “4️⃣ Test de /api/docker”
curl -s “$API_URL/api/docker” | python3 -m json.tool
echo “”

echo “✅ Tests terminés”
TESTAPI

chmod +x dashboard/test_api.sh

# ==========================================

# Affichage de la structure créée

# ==========================================

echo “”
echo -e “${GREEN}✅ Structure créée avec succès !${NC}”
echo “”
echo -e “${BLUE}📂 Structure des fichiers :${NC}”
tree dashboard/ 2>/dev/null || find dashboard/ -type f

echo “”
echo -e “${BLUE}==========================================”
echo “  📋 PROCHAINES ÉTAPES”
echo “==========================================${NC}”
echo “”
echo “1️⃣  Aller dans le répertoire :”
echo “   cd services/dashboard”
echo “”
echo “2️⃣  Tester en local (optionnel) :”
echo “   pip install -r requirements.txt”
echo “   python main.py”
echo “”
echo “3️⃣  Ou builder avec Docker :”
echo “   docker build -t dashboard-backend .”
echo “   docker run -p 8000:8000 -v /var/run/docker.sock:/var/run/docker.sock dashboard-backend”
echo “”
echo “4️⃣  Ou avec Docker Compose :”
echo “   cd ../..”
echo “   docker-compose build dashboard-backend”
echo “   docker-compose up -d dashboard-backend”
echo “”
echo “5️⃣  Vérifier les logs :”
echo “   docker-compose logs -f dashboard-backend”
echo “”
echo “6️⃣  Tester l’API :”
echo “   ./services/dashboard/test_api.sh”
echo “”
echo -e “${GREEN}✨ Tout est prêt ! Bonne chance ! 🚀${NC}”
