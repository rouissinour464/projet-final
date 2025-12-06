
#!/bin/bash
NODE_IP=$(kubectl get nodes -o wide | awk 'NR==2{print $6}')
echo "Ajout de données initiales..."

# Ajouter un utilisateur
curl -X POST http://$NODE_IP:30080/users \
-H "Content-Type: application/json" \
-d '{"name":"Alice","email":"alice@example.com"}'

# Ajouter une statistique
curl -X POST http://$NODE_IP:30080/stats \
-H "Content-Type: application/json" \
-d '{"metric":"visits","value":100}'
