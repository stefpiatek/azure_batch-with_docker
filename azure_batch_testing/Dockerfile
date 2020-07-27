FROM continuumio/miniconda3:4.8.2

WORKDIR /azure_batch_testing
COPY requirements_dev.txt /azure_batch_testing/requirements_dev.txt

RUN pip install -r requirements_dev.txt

COPY . /azure_batch_testing
RUN pip install -e .
