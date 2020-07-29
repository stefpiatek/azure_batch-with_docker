
# portal/CLI

create new registry, in this case, `steftest` (done in the portal)


# Build and push image to azure docker registry

```shell script

cd azure_batch_testing

docker login --username=stefpiatek --password=""

export DOCKER_ACC=steftest.azurecr.io
export DOCKER_REPO=azure_docker

# build local image, tagging version for azure and push
docker build -t $DOCKER_ACC/$DOCKER_REPO:0.1.0 .
docker push $DOCKER_ACC/$DOCKER_REPO:0.1.0

# remove local image
docker rmi $DOCKER_ACC/$DOCKER_REPO:0.1.0

```

## Create service principle and add permissions

Set owner permissions for the subscriptions

[create a service principle](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)

Had to use portal to create and configure service principle, didn't have permissions to create them on the CLI

- Through `Enterprise Appliatcions`, create new application (service principle)
    - Service principle made with any accounts in organisational directory, multitenant
- In `Subscription`, use `Access control (IAM)` to add contributor role to service principle
- Created a new application secret for service principle

# Useful links for creating 

[container workloads](https://docs.microsoft.com/en-gb/azure/batch/batch-docker-container-workloads)
