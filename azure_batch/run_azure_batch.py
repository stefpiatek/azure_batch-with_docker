# sample2_pools_and_resourcefiles.py Code Sample
#
# Copyright (c) Microsoft Corporation
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import configparser
import datetime
import os
from pathlib import Path

import azure.batch._batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels
import azure.storage.blob as azureblob
from azure.batch.models import ContainerWorkingDirectory, TaskContainerSettings
from common import helpers as azure_helpers

_CONTAINER_NAME = 'dockerbatchstorage'


def create_pool_and_add_tasks(batch_client, block_blob_client, pool_id, vm_size, vm_count, registry_config, job_id):
    """Creates an Azure Batch pool with the specified id.

    :param batch_client: The batch client to use.
    :type batch_client: `batchserviceclient.BatchServiceClient`
    :param block_blob_client: The storage block blob client to use.
    :type block_blob_client: `azure.storage.blob.BlockBlobService`
    :param str pool_id: The id of the pool to create.
    :param str vm_size: vm size (sku)
    :param int vm_count: number of vms to allocate
    """
    # pick the latest supported 16.04 sku for UbuntuServer
    sku_to_use, image_ref_to_use = azure_helpers.select_latest_verified_vm_image_with_node_agent_sku(
        batch_client, 'microsoft-azure-batch', 'ubuntu-server-container', '16-04-lts')

    # define docker image to use
    container_registry = batch.models.ContainerRegistry(
        **registry_config
    )

    container_conf = batch.models.ContainerConfiguration(
        container_image_names=[f"{registry_config['registry_server']}/azure_docker:0.1.0"],
        container_registries=[container_registry]
    )

    container_settings = TaskContainerSettings(
        image_name=f"{registry_config['registry_server']}/azure_docker:0.1.0",
        registry=container_registry,
        container_run_options="--rm",
        working_directory=ContainerWorkingDirectory.task_working_directory
    )

    # define main tasks, including input and outputs
    tasks = []
    resource_files = []
    for task_script in ["petal_width.py", "sepal_width.py"]:
        # upload resource files
        task_name = task_script.replace("_", "")
        task_path = Path("resources", task_script)
        script_stem = task_script.rstrip(".py")

        sas_url = azure_helpers.upload_blob_and_create_sas(
            block_blob_client,
            _CONTAINER_NAME,
            task_name,
            task_path,
            datetime.datetime.utcnow() + datetime.timedelta(hours=1))

        resource_file = batchmodels.ResourceFile(
            file_path=task_name,
            http_url=sas_url)
        resource_files.append(resource_file)

        # output data to upload to storage container
        container_url = azure_helpers.create_container_sas(
            block_blob_client,
            _CONTAINER_NAME,
            datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        )
        output_file = batchmodels.OutputFile(
            file_pattern=f'output/{script_stem}.csv',
            destination=batchmodels.OutputFileDestination(
                container=batchmodels.OutputFileBlobContainerDestination(
                    container_url=container_url,
                    path=f'{job_id}/output/{script_stem}.csv'
                )
            ),
            upload_options=batchmodels.OutputFileUploadOptions(
                upload_condition=batchmodels.OutputFileUploadCondition.task_completion
            )
        )

        # add tasks with resources and outputs
        tasks.append(batchmodels.TaskAddParameter(
            id=script_stem,
            command_line=f'python3 {task_name}',
            resource_files=[resource_file],
            container_settings=container_settings,
            output_files=[output_file]
        ))

    pool = batchmodels.PoolAddParameter(
        id=pool_id,
        virtual_machine_configuration=batchmodels.VirtualMachineConfiguration(
            image_reference=image_ref_to_use,
            container_configuration=container_conf,
            node_agent_sku_id=sku_to_use),
        vm_size=vm_size,
        max_tasks_per_node=1,
        target_dedicated_nodes=vm_count,
        start_task=batchmodels.StartTask(
            command_line="",
            resource_files=resource_files,
            wait_for_success=True,
            container_settings=container_settings),
    )

    azure_helpers.create_pool_if_not_exist(batch_client, pool)

    job = batchmodels.JobAddParameter(
        id=job_id,
        pool_info=batchmodels.PoolInformation(pool_id=pool_id))

    batch_client.job.add(job)

    # Add tasks to batch client, under the same job
    batch_client.task.add_collection(job_id=job.id, value=tasks)


def execute_sample(global_config, sample_config):
    """Executes the sample with the specified configurations.

    :param global_config: The global configuration to use.
    :type global_config: `configparser.ConfigParser`
    :param sample_config: The sample specific configuration to use.
    :type sample_config: `configparser.ConfigParser`
    """
    # Set up the configuration
    batch_account_key = global_config.get('Batch', 'batchaccountkey')
    batch_account_name = global_config.get('Batch', 'batchaccountname')
    batch_service_url = global_config.get('Batch', 'batchserviceurl')

    storage_account_key = global_config.get('Storage', 'storageaccountkey')
    storage_account_name = global_config.get('Storage', 'storageaccountname')
    storage_account_suffix = global_config.get(
        'Storage',
        'storageaccountsuffix')

    should_delete_container = sample_config.getboolean(
        'DEFAULT',
        'shoulddeletecontainer')
    should_delete_job = sample_config.getboolean(
        'DEFAULT',
        'shoulddeletejob')
    should_delete_pool = sample_config.getboolean(
        'DEFAULT',
        'shoulddeletepool')
    pool_vm_size = sample_config.get(
        'DEFAULT',
        'poolvmsize')
    pool_vm_count = sample_config.getint(
        'DEFAULT',
        'poolvmcount')

    # Print the settings we are running with
    azure_helpers.print_configuration(global_config)
    azure_helpers.print_configuration(sample_config)

    credentials = batchauth.SharedKeyCredentials(
        batch_account_name,
        batch_account_key)
    batch_client = batch.BatchServiceClient(
        credentials,
        batch_url=batch_service_url)

    # Retry 5 times -- default is 3
    batch_client.config.retry_policy.retries = 5

    block_blob_client = azureblob.BlockBlobService(
        account_name=storage_account_name,
        account_key=storage_account_key,
        endpoint_suffix=storage_account_suffix)

    job_id = azure_helpers.generate_unique_resource_name(
        "DockerBatchTesting2221Job")
    pool_id = "DockerBatchTesting2221Pool"
    registry_config = {
        'registry_server': global_config.get('Registry', 'registryname'),
        'user_name': global_config.get('Registry', 'username'),
        'password': global_config.get('Registry', 'password'),
    }
    try:
        create_pool_and_add_tasks(
            batch_client,
            block_blob_client,
            pool_id,
            pool_vm_size,
            pool_vm_count,
            registry_config,
            job_id)

        azure_helpers.wait_for_tasks_to_complete(
            batch_client,
            job_id,
            datetime.timedelta(minutes=25))

        tasks = batch_client.task.list(job_id)
        task_ids = [task.id for task in tasks]

        azure_helpers.print_task_output(batch_client, job_id, task_ids)
    finally:
        # clean up
        # if should_delete_container:
        #     block_blob_client.delete_container(
        #         _CONTAINER_NAME,
        #         fail_not_exist=False)
        # if should_delete_job:
        #     print("Deleting job: ", job_id)
        #     batch_client.job.delete(job_id)
        # if should_delete_pool:
        #     print("Deleting pool: ", pool_id)
        #     batch_client.pool.delete(pool_id)
        pass


if __name__ == '__main__':
    global_config = configparser.ConfigParser()
    global_config.read(azure_helpers._SAMPLES_CONFIG_FILE_NAME)

    sample_config = configparser.ConfigParser()
    sample_config.read(
        os.path.splitext(os.path.basename(__file__))[0] + '.cfg')

    execute_sample(global_config, sample_config)
