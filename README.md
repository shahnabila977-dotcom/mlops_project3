# Kubernetes & MLOps Workflow Project

## Workflow
Terraform -> Minikube -> Jenkins -> MLflow -> Load Balancer / Kubernetes

## Structure
- `infra/`: Terraform configuration (`providers.tf`, `variables.tf`, `main.tf`)
- `manifests/`: Kustomize manifests (`kustomization.yaml`, `deployment.yaml`, `service.yaml`)
- `pipeline/`: Kubeflow pipeline (`iris_pipeline.py` -> `iris_pipeline.yaml`) and MLflow registry script (`register_model.py`)
- `nginx/`: NGINX load balancer configuration (`ml_loadbalancer.conf`)
- `Jenkinsfile`: Pipeline automation steps
