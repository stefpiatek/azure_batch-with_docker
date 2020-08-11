FROM continuumio/miniconda3:4.8.2

WORKDIR /azure_batch/azure_batch_testing
COPY docker/requirements_dev.txt /azure_batch/azure_batch_testing/requirements_dev.txt

RUN pip install -r requirements_dev.txt

COPY docker /azure_batch/azure_batch_testing
RUN pip install -e .

COPY . /azure_batch

CMD /bin/bash checkout_git.sh && /bin/bash
