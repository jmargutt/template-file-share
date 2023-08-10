# template-blob-storage
Template of Dockerized Python application to download/upload data from/to Azure blob storage.

## setup
1. Add the name of your container and the connection string as environment variables (credentials/.env).
2. Add what you need in pipeline.py:main.
3install and run locally
```
cd pipeline
pip install .
run-pipeline
```
Or build docker container and push it to Azure Container Registry
```
az acr login -n myregistry
docker build -t myregistry.azurecr.io/template-blob-storage .
docker image push myregistry.azurecr.io/template-blob-storage
```