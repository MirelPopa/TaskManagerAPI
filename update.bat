minikube image build -t fastapi -f Dockerfile.api .
minikube image build -t worker -f Dockerfile.worker .
minikube image load fastapi:latest
minikube image load worker:latest
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml
minikube service fastapi
