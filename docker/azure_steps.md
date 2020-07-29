
# portal/CLI

create new registry, in this case, `steftest` (done in the portal)


## currently failing - add pull permissions to the container registry

Set owner permissions for the subscriptions

[set azure subscription permissions](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#check-azure-subscription-permissions)



[create a service principle](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-auth-service-principal#create-a-service-principal)
```shell script

# ACR_NAME: The name of your Azure Container Registry
# SERVICE_PRINCIPAL_NAME: Must be unique within your AD tenant
ACR_NAME=steftest
SERVICE_PRINCIPAL_NAME=acr-service-principal
# login to registry
az acr login --name $ACR_NAME


# Create the service principal with rights scoped to the registry.
# Default permissions are for docker pull access. Modify the '--role'
# argument value as desired:
# acrpull:     pull only
# acrpush:     push and pull
# owner:       push, pull, and assign roles

# Obtain the full registry ID for subsequent command args
ACR_REGISTRY_ID=$(az acr show --name $ACR_NAME --query id --output tsv)



SP_PASSWD=$(az ad sp create-for-rbac --name http://$SERVICE_PRINCIPAL_NAME --scopes $ACR_REGISTRY_ID --role acrpull --query password --output tsv)
## fails here because no permission to create the service principle
SP_APP_ID=$(az ad sp show --id http://$SERVICE_PRINCIPAL_NAME --query appId --output tsv)

# Output the service principal's credentials; use these in your services and
# applications to authenticate to the container registry.
echo "Service principal ID: $SP_APP_ID"
echo "Service principal password: $SP_PASSWD"
```


# Build and push image to azure docker registry


```shell script

cd azure_batch_testing

docker login --username=stefpiatek --password=""

export DOCKER_ACC=steftest.azurecr.io
export DOCKER_REPO=azure_docker

# build local image, tagging version for azure and push
docker build -t $DOCKER_ACC/$DOCKER_REPO:0.1.0 .
docker push $DOCKER_ACC/$DOCKER_REPO:0.1.0

# also build and push to dockerhub for testing while trying to work out access to azure container registry
export DOCKERHUB_ACC=stefpiatek
docker build -t $DOCKERHUB_ACC/$DOCKER_REPO:0.1.0 .
docker push $DOCKERHUB_ACC/$DOCKER_REPO:0.1.0

# remove local image
docker rmi $DOCKER_ACC/$DOCKER_REPO:0.1.0

```
