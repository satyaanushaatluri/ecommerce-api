# Kubernetes (Starter) — ecommerce-api

## What is here
- `deployment.yaml` — 2 replicas of the FastAPI app on port 8000.
- `service.yaml` — ClusterIP Service (internal only, not public).

## Before you apply
1. Build and push the image to the ECR repository from `terraform/main.tf`,
   then replace the `<registry>/ecommerce-api:latest` placeholder in `deployment.yaml`
   with the real ECR URL (`terraform apply` prints it as `ecr_repository_url`).
2. Create the database secret (replace the URL with your real database):
   ```bash
   kubectl create secret generic ecommerce-api-db-secret \
     --from-literal=DATABASE_URL='postgresql://user:pass@db-host:5432/appdb'
   ```

## Apply
```bash
kubectl apply -f k8s/
kubectl get pods -l app=ecommerce-api
kubectl port-forward svc/ecommerce-api 8000:80
```
Then open http://127.0.0.1:8000/docs

## Notes
- ClusterIP is internal to the cluster. For public access, add an Ingress
  or change the Service type — that is not included in this starter.
- Committing these files deploys nothing on its own; `kubectl apply` does.
