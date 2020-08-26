
# portal/CLI

create new registry, in this case, `steftest` (done in the portal)


# Build and push image to docker hub

```shell script

export DOCKER_ACC=stefpiatek
export DOCKER_REPO=azure_docker
export DOCKER_TAG=0.1.0

docker login --username=${DOCKER_ACC} --password=""

# build local image, tagging version for azure and push
docker build -t ${DOCKER_ACC}/${DOCKER_REPO}:${DOCKER_TAG} .
docker push ${DOCKER_ACC}/${DOCKER_REPO}:${DOCKER_TAG}

# remove local image
docker rmi ${DOCKER_ACC}/${DOCKER_REPO}:${DOCKER_TAG}

```

# Useful links for creating 

[container workloads](https://docs.microsoft.com/en-gb/azure/batch/batch-docker-container-workloads)

# No longer needed

Can preload dockerhub private images so no benefit in using azure container registry

## Create service principle and add permissions

Set owner permissions for the subscriptions

[create a service principle](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)

Had to use portal to create and configure service principle, didn't have permissions to create them on the CLI

- Through `Enterprise Appliatcions`, create new application (service principle)
    - Service principle made with any accounts in organisational directory, multitenant
- In `Subscription`, use `Access control (IAM)` to add contributor role to service principle
- Created a new application secret for service principle


