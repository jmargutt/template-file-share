# template-file-share
Template of Dockerized Python application to download/upload data from/to Azure File Share.

## setup
1. Add the name of your file share, the storage account name and the storage account key as environment variables (credentials/.env).
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
docker build -t myregistry.azurecr.io/template-file-share .
docker image push myregistry.azurecr.io/template-file-share
```