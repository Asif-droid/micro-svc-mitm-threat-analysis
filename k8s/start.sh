kubectl apply -f flask-app-deployment-def.yml
kubectl apply -f flask-app2-deployment-def.yml
kubectl apply -f istio-gateway-def.yml

## attack
# kubectl apply -f mitm-attacker.yml
# kubectl delete service flask-app-2
# kubectl delete service mitm-flask-app-2
# kubectl expose deployment mitm-proxy --name=flask-app-2 --port=5001--target-port=5001
# kubectl expose deployment flask-app-2 --name=flask-app-2-backup --port=5001 --target-port=5001



