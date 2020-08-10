# Azure Batch using Docker containers

Prototype project for running a Docker container in Azure batch.

## Python package and Dockerfile

- located in [docker](/docker) 
- contains a cookie cutter-produced python package 
  that is imported and used by each task
- Dockerfile installs this package from miniconda
- Other steps required in [docker/azure_steps.md](/docker/azure_steps.md):
    - The docker image was built and then pushed to the azure container registry
    - Created a service principle to allow for automated pulling of the docker container 
      by each node in azure batch 
      (had to be done in the portal, CLI steps complained about lack of permissions)


## Running in azure batch

- Using python API for azure batch, in [azure_batch](/azure_batch)
- Reused some azure batch examples helper functions, so copied to [azure_batch/common](/azure_batch/common)
- Two scripts to be run in a task are in [azure_batch/resources](/azure_batch/resources)

Main runner in [azure_batch/run_azure_batch.py](/azure_batch/run_azure_batch.py)

- Gets all configuration details
- Uses docker-compatible VMs for each node - `'microsoft-azure-batch', 'ubuntu-server-container', '16-04-lts'`
- Defines the docker image from the azure container registry, and docker run settings
- Creates processing tasks and then a post-processing task which takes the output of 
  the two tasks and uses them
- Creates a pool using the defined VM, docker container and can define a starting tasks here too
    - maximum of one task per node to force parallel tasks
- creates a job to run on the pool
- Adds all tasks to the job

## Areas not yet addressed

- Copying of files from azure storage to local machine after post-processing.
  This should be simple enough but just didn't get around to it
- A pre-run check to make sure that before submitting the entire job, it will run without failure.
  Haven't really seen a way around this so far. 

  
 