
# portal/CLI

create new registry, in this case, `steftest`

login to registry

```shell script
az acr login --name steftest
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

# remove local image
docker rmi $DOCKER_ACC/$DOCKER_REPO:0.1.0

```
