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

echo -e “’033[0📝 Création de requirements.txt…’033[0m’”
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

echo -e “’033[0📝 Création de Dockerfile…’033[0m’”
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

echo -e “’033[0📝 Création de app/**init**.py…’033[0m’”
cat > dashboard/app/**init**.py << ‘APPINIT’

# Fichier vide pour marquer app comme un package Python

APPINIT

# ==========================================

# 5. app/api/**init**.py

# ==========================================

echo -e “’033[0📝 Création de app/api/**init**.py…’033[0m’”
cat > dashboard/app/api/**init**.py << ‘APIINIT’

# Fichier vide pour marquer app/api comme un package Python

APIINIT

# ==========================================

# 6. app/api/health.py

# ==========================================

echo -e “’033[0📝 Création de app/api/health.py…’033[0m’”
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

echo -e “’033[0📝 Création de app/api/system.py…’033[0m’”
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



SYSTEMPY

# ==========================================

# 8. app/api/docker.py

# ==========================================

echo -e “’033[0📝 Création de app/api/docker.py…’033[0m’”
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



@router.post(”/docker/{container_name}/start”)
def start_container(container_name: str):
“”“Démarre un conteneur”””
try:
client = get_docker_client()
container = client.containers.get(container_name)



@router.post(”/docker/{container_name}/stop”)
def stop_container(container_name: str):
“”“Arrête un conteneur”””
try:
client = get_docker_client()
container = client.containers.get(container_name)



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



DOCKERPY

# ==========================================

# 9. .dockerignore

# ==========================================

echo -e “’033[0📝 Création de .dockerignore…’033[0m’”
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

echo -e “’033[0📝 Création de .gitignore…’033[0m’”
cat > dashboard/.gitignore << ‘GITIGNORE’

# Python

**pycache**/
*.py[cod]
*.class
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

echo -e “’033[0📝 Création de README.md…’033[0m’”
cat > dashboard/README.md << ‘README’

# Dashboard Service

Service de monitoring système et Docker pour Homebox.

## 🚀 Démarrage rapide

### Avec Docker Compose

dashboard
HEAD is now at b71aca4 feat(frontend): normalisation API pour le dashboard HomeBox
On branch feature/api-normalisation
Your branch is behind 'origin/feature/api-normalisation' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	services/dashboard/backend/api/
	services/dashboard/backend/main.py
	services/dashboard/backend/services/
	services/dashboard/backend/test.sh

nothing added to commit but untracked files present (use "git add" to track)
[H[2J[3J#1 [internal] load local bake definitions
#1 reading from stdin 1.08kB done
#1 DONE 0.0s

#2 [dashboard-frontend internal] load build definition from Dockerfile
#2 transferring dockerfile: 280B done
#2 ...

#3 [dashboard-backend internal] load build definition from Dockerfile
#3 transferring dockerfile: 519B done
#3 DONE 0.2s

#2 [dashboard-frontend internal] load build definition from Dockerfile
#2 DONE 0.6s

#4 [dashboard-frontend internal] load metadata for docker.io/library/node:20
#4 DONE 0.0s

#5 [dashboard-frontend internal] load metadata for docker.io/library/nginx:stable-alpine
#5 DONE 1.1s

#6 [dashboard-backend internal] load metadata for docker.io/library/python:3.11-slim
#6 ...

#7 [dashboard-frontend internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.2s

#6 [dashboard-backend internal] load metadata for docker.io/library/python:3.11-slim
#6 DONE 1.5s

#8 [dashboard-frontend internal] load build context
#8 DONE 0.0s

#9 [dashboard-frontend stage-1 1/2] FROM docker.io/library/nginx:stable-alpine@sha256:30f1c0d78e0ad60901648be663a710bdadf19e4c10ac6782c235200619158284
#9 DONE 0.0s

#10 [dashboard-frontend build 1/6] FROM docker.io/library/node:20
#10 DONE 0.0s

#11 [dashboard-backend internal] load .dockerignore
#11 transferring context: 2B done
#11 DONE 0.3s

#8 [dashboard-frontend internal] load build context
#8 ...

#12 [dashboard-backend internal] load build context
#12 transferring context: 192B 0.1s done
#12 DONE 0.4s

#13 [dashboard-backend 1/6] FROM docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c
#13 resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c 0.4s done
#13 DONE 0.4s

#14 [dashboard-backend 2/6] WORKDIR /app
#14 CACHED

#15 [dashboard-backend 3/6] RUN apt-get update && apt-get install -y     gcc     && rm -rf /var/lib/apt/lists/*
#15 CACHED

#16 [dashboard-backend 4/6] COPY requirements.txt .
#16 CACHED

#17 [dashboard-backend 5/6] RUN pip install --no-cache-dir -r requirements.txt
#17 CACHED

#18 [dashboard-backend 6/6] COPY app.py .
#18 CACHED

#8 [dashboard-frontend internal] load build context
#8 ...

#19 [dashboard-backend] exporting to image
#19 exporting layers done
#19 writing image sha256:b892829d7c9951e393ba66de666a6bd360216f867fd24c0034c51a17e593f750 0.0s done
#19 naming to docker.io/library/dashboard-dashboard-backend 0.1s done
#19 DONE 0.2s

#8 [dashboard-frontend internal] load build context
#8 ...

#20 [dashboard-backend] resolving provenance for metadata file
#20 DONE 0.0s

#8 [dashboard-frontend internal] load build context
#8 transferring context: 3.01MB 2.4s done
#8 DONE 2.7s

#21 [dashboard-frontend build 2/6] WORKDIR /app
#21 CACHED

#22 [dashboard-frontend build 3/6] COPY package.json package-lock.json ./
#22 CACHED

#23 [dashboard-frontend build 4/6] RUN npm install
#23 CACHED

#24 [dashboard-frontend build 5/6] COPY . .
#24 CACHED

#25 [dashboard-frontend build 6/6] RUN npm run build
#25 CACHED

#26 [dashboard-frontend stage-1 2/2] COPY --from=build /app/build /usr/share/nginx/html
#26 CACHED

#27 [dashboard-frontend] exporting to image
#27 exporting layers done
#27 writing image sha256:01d644285270f488cd04565aa50f553266955f683c0354e6e6da798010c8e929 0.1s done
#27 naming to docker.io/library/dashboard-dashboard-frontend
#27 naming to docker.io/library/dashboard-dashboard-frontend 0.0s done
#27 DONE 0.2s

#28 [dashboard-frontend] resolving provenance for metadata file
#28 DONE 0.0s

### En local (développement)



## 📡 Endpoints

- <HTML>
<HEAD>
<TITLE>Directory /</TITLE>
<BASE HREF="file:/">
</HEAD>
<BODY>
<H1>Directory listing of /</H1>
<UL>
<LI><A HREF="./">./</A>
<LI><A HREF="../">../</A>
<LI><A HREF="PATH_TO_YOUR_CONFIG/">PATH_TO_YOUR_CONFIG/</A>
<LI><A HREF="bin/">bin/</A>
<LI><A HREF="bin.usr-is-merged/">bin.usr-is-merged/</A>
<LI><A HREF="boot/">boot/</A>
<LI><A HREF="cdrom/">cdrom/</A>
<LI><A HREF="dev/">dev/</A>
<LI><A HREF="dossier_docker/">dossier_docker/</A>
<LI><A HREF="etc/">etc/</A>
<LI><A HREF="hme/">hme/</A>
<LI><A HREF="home/">home/</A>
<LI><A HREF="homebox/">homebox/</A>
<LI><A HREF="lib/">lib/</A>
<LI><A HREF="lib.usr-is-merged/">lib.usr-is-merged/</A>
<LI><A HREF="lib64/">lib64/</A>
<LI><A HREF="lost%2Bfound/">lost+found/</A>
<LI><A HREF="media/">media/</A>
<LI><A HREF="mnt/">mnt/</A>
<LI><A HREF="opt/">opt/</A>
<LI><A HREF="proc/">proc/</A>
<LI><A HREF="prometheus.yml/">prometheus.yml/</A>
<LI><A HREF="root/">root/</A>
<LI><A HREF="run/">run/</A>
<LI><A HREF="sbin/">sbin/</A>
<LI><A HREF="sbin.usr-is-merged/">sbin.usr-is-merged/</A>
<LI><A HREF="snap/">snap/</A>
<LI><A HREF="srv/">srv/</A>
<LI><A HREF="swap.img">swap.img</A>
<LI><A HREF="sys/">sys/</A>
<LI><A HREF="tmp/">tmp/</A>
<LI><A HREF="usr/">usr/</A>
<LI><A HREF="var/">var/</A>
</UL>
</BODY>
</HTML> - Info service
-  - Health check
-  - Statistiques système (CPU, RAM, Disque, Température)
-  - Liste des conteneurs Docker
-  - Démarrer un conteneur
-  - Arrêter un conteneur
-  - Redémarrer un conteneur

## 🧪 Tests



## 📋 Requirements

- Python 3.11+
- Docker (pour le monitoring des conteneurs)
- Accès au socket Docker ()

## 🔧 Configuration

Variables d’environnement (optionnelles) :

-  - Port du service (défaut: 8000)
-  - Host d’écoute (défaut: 0.0.0.0)

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

echo -e “’033[0📝 Création de test_api.sh…’033[0m’”
cat > dashboard/test_api.sh << ‘TESTAPI’
#!/bin/bash

API_URL=”http://localhost:8000”

echo “🧪 Test de l’API Dashboard sur ”
echo “”

# Test 1: Root

echo “1️⃣ Test de /”
curl -s “/” | python3 -m json.tool
echo “”

# Test 2: Health

echo “2️⃣ Test de /api/health”
curl -s “/api/health” | python3 -m json.tool
echo “”

# Test 3: System

echo “3️⃣ Test de /api/system”
curl -s “/api/system” | python3 -m json.tool
echo “”

# Test 4: Docker

echo “4️⃣ Test de /api/docker”
curl -s “/api/docker” | python3 -m json.tool
echo “”

echo “✅ Tests terminés”
TESTAPI

chmod +x dashboard/test_api.sh

# ==========================================

# Affichage de la structure créée

# ==========================================

echo “”
echo -e “’033[0✅ Structure créée avec succès !’033[0m’”
echo “”
echo -e “’033[0📂 Structure des fichiers :’033[0m’”
tree dashboard/ 2>/dev/null || find dashboard/ -type f

echo “”
echo -e “’033[0==========================================”
echo “  📋 PROCHAINES ÉTAPES”
echo “==========================================’033[0m’”
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
echo -e “’033[0✨ Tout est prêt ! Bonne chance ! 🚀’033[0m’”
