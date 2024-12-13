# ML Pipeline with Great Expectations

## Prerequisites

- Install [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- Install [Helm](https://helm.sh/docs/intro/install/)
- Docker Hub account (for building/pushing images)

## Installation

1. **Create kind cluster**

```bash
kind create cluster --config cluster.yaml
```

2. **Set up environment variables**

```bash
# Required for Helm chart installation
export GX_CLOUD_ORGANIZATION_ID=your_org_id
export GX_CLOUD_ACCESS_TOKEN=your_access_token
```

3. **Install using Helm**

```bash
# Install the chart
helm install ml-pipeline ./mychart \
  --set gxCloud.organizationId=$GX_CLOUD_ORGANIZATION_ID \
  --set gxCloud.accessToken=$GX_CLOUD_ACCESS_TOKEN

# Verify installation
kubectl get pods
kubectl get services
```

## Development

### Building Docker Images

```bash
# Log in to DockerHub
docker login -u oswaldodocker

# Build images
docker build -f ./environment/notebook.Dockerfile -t oswaldodocker/notebook:v3 ./environment
docker build -f ./environment/datadocs.Dockerfile -t oswaldodocker/datadocs:v3 ./environment
docker build -f ./environment/mlflow.Dockerfile -t oswaldodocker/mlflow:v3 ./environment

# Push images
docker push oswaldodocker/notebook:v3
docker push oswaldodocker/datadocs:v3
docker push oswaldodocker/mlflow:v3
```

### Port Forwarding

Access the services locally:

```bash
kubectl port-forward svc/notebook-service 8888:8888 &
kubectl port-forward svc/mlflow-service 5000:5000 &
kubectl port-forward svc/mlflow-service 5555:5555 &
```

### Troubleshooting

Check pod status and logs:

```bash
# Check pod status
kubectl get pods

# View logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

### Cleanup

```bash
# Uninstall the Helm release
helm uninstall ml-pipeline

# Delete the cluster if needed
kind delete cluster
```