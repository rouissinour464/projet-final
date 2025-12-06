
#!/bin/bash
echo "Déploiement des microservices sur Kubernetes..."
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/user-service/
kubectl apply -f k8s/stats-service/
kubectl apply -f k8s/postgres/
echo "✅ Déploiement terminé !"
