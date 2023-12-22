# Torchserve Docker CICD 

This repository contains the code for Torchserve Docker CICD. It includes a Torchserve deployment file, instructions for running the Docker container, a custom handler for processing inputs and running inference, a HuggingFace model created in the `conll2023.ipynb` file, and a Dockerfile for building the container.

## Getting Started

To get started with this project, follow the instructions below.

### What is a mar file?

The mar file is a model archive file that contains the model, the handler, and the dependencies. It is used by Torchserve to load the model and run inference on it. It basically groups all the files needed to run the model in one file.

## Steps we took to create this project

1. Create a repository for the project with the dependencies and clone the torchserve repository

2. Create a custom handler for processing inputs and running inference

3. Create a model

4. Create test cases for the model

5. Create the mar file on the server so you don't have to add a big model in the final Docker image

6. Create a Dockerfile for building the container

7. Create a github actions workflow file for building and pushing the container to Dockerhub

8. Add branch protection rules to the github repository applying the tests

9. Run the workflow on a self-hosted runner so you don't have to push a big model to github

## Usage

1. On the server, pull the container from Dockerhub and run it using the following command:

```bash

docker run -v /path/to/your/log/directory:/home/model-server/logs your_docker_image
    
```
where `/path/to/your/log/directory` is the path to the directory where you want to store the logs and `your_docker_image` is the name of the Docker image you created in step 5.

2. Run inference on the deployed model by sending requests to the appropriate endpoint. The endpoint is `http://localhost:8080/predictions/<model_name>`, where `<model_name>` is the name of the model you specified in the `config.properties` file. In our case NER_BERT_model. 

3. send a POST request to the endpoint with the following body:

```bash
{
    "input": ["your text here","some more text here maybe ?"]
}
```
4. Congrats you have succesfully loaded a model and ran inference on it using torchserve.

## Docker container file structure
    
```bash
/
|-- home
|   |-- model-server
|       |-- model-store
|           |-- NER_BERT_Model.mar
|       |-- config.properties
|       |-- requirements.txt

```
# Created by 

- Rami Kassouf
- Marie Assine Ghantous
- Robin Nabhan