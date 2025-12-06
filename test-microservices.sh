
#!/bin/bash
NODE_IP=$(kubectl get nodes -o wide | awk 'NR==2{print $6}')
echo "Test des microservices..."

# Vérifier le frontend
curl http://$NODE_IP:30080

# Vérifier User Service
curl http://$NODE_IP:30080/users

# Vérifier Stats Service
curl http://$NODE_IP:30080/stats
