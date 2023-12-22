# Torchserve Docker CICD 

This repository contains the code for Torchserve Docker CICD. It includes a Torchserve deployment file, instructions for running the Docker container, a custom handler for processing inputs and running inference, a HuggingFace model created in the `conll2023.ipynb` file, and a Dockerfile for building the container.

## Getting Started

To get started with this project, follow the instructions below.

## Steps we took to create this project

1. Create a repository for the project with the dependencies and clone the torchserve repository

2. Create a custom handler for processing inputs and running inference

3. Create a model

4. Create test cases for the model

5. Create a Dockerfile for building the container

6. Create a github actions workflow file for building and pushing the container to Dockerhub

7. Add branch protection rules to the github repository applying the tests

8. Run the workflow on a self-hosted runner so you don't have to push a big model to github

## Usage

1. On the server, pull the container from Dockerhub and run it using the following command:

```bash

docker run -v /path/to/your/log/directory:/home/model-server/logs your_docker_image
    
```
where `/path/to/your/log/directory` is the path to the directory where you want to store the logs and `your_docker_image` is the name of the Docker image you created in step 5.

2. Run inference on the deployed model by sending requests to the appropriate endpoint. The endpoint is `http://localhost:8080/predictions/<model_name>`, where `<model_name>` is the name of the model you specified in the `config.properties` file. In our case NER_BERT_model.


## Docker container file structure
    
```bash
/
|-- home
|   |-- model-server
|       |-- model-store
|       |-- logs
|       |-- NER_BERT_Model
|           |-- pytorch_model.bin
|           |-- config.json
|           |-- special_tokens_map.json
|           |-- tokenizer_config.json
|           |-- tokenizer.json
|       |-- ner_handler.py
|       |-- index_to_name.json
|       |-- requirements.txt

```
# Created by 

- Rami Kassouf
- Marie Assine Ghantous
- Robin Nabhan