# PROJET-FINAL-MAIN – Microservices avec
Kubernetes et PostgreSQL
## ■ Description
Ce projet implémente une architecture microservices déployée sur Kubernetes avec :
- Frontend Service : Interface utilisateur (HTML + Flask).
- User Service : Gestion des utilisateurs.
- Stats Service : Gestion des statistiques.
- PostgreSQL : Base de données persistante.
Chaque service est conteneurisé avec Docker et orchestré via Kubernetes (Deployments, Services,
ConfigMaps, Secrets, StatefulSets).
## ■ Architecture Globale
Frontend → User Service → PostgreSQL
Frontend → Stats Service → PostgreSQL
## ■ Structure du projet
PROJET-FINAL-MAIN/
├── frontend-service/
│   ├── templates/index.html
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── user-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── stats-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── postgres/init/init.sql
├── k8s/
│   ├── frontend/
│   │   ├── frontend-configmap.yaml
│   │   ├── frontend-deployment.yaml
│   │   └── frontend-service.yaml
│   ├── user-service/
│   │   ├── user-configmap.yaml
│   │   ├── user-deployment.yaml
│   │   └── user-service.yaml
│   ├── stats-service/
│   │   ├── stats-configmap.yaml
│   │   ├── stats-deployment.yaml
│   │   └── stats-service.yaml
│   └── postgres/
│       ├── postgres-secret.yaml
│       ├── postgres-service.yaml
│       └── postgres-statefulset.yaml
└── docker-compose.yml
## ■ Déploiement
### Option 1 : Docker Compose
```
docker-compose up --build
```
### Option 2 : Kubernetes
```
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/user-service/
kubectl apply -f k8s/stats-service/
kubectl apply -f k8s/frontend/
```
## ■ Endpoints
- Frontend : http://:30080
- User Service : GET /users, POST /users
- Stats Service : GET /stats, POST /stats
## ■ Base de données
PostgreSQL avec init.sql pour créer les tables :
- users(id, name, email)
- stats(id, metric, value)
## ■ Diagramme Architecture
Frontend → API → Services → PostgreSQL
Architecture Diagram
+-------------------+       +-------------------+
|   Frontend        | --->  |   User Service    |
| (Flask + HTML)    |       | (Flask API)       |
+-------------------+       +-------------------+
         |                          |
         v                          v
+-------------------+       +-------------------+
|   Stats Service   | --->  |   PostgreSQL DB   |
| (Flask API)       |       | (StatefulSet)     |
+-------------------+       +-------------------+
