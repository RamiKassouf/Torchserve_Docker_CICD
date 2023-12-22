FROM pytorch/torchserve:latest-cpu

# Create the directories for the model store
RUN mkdir -p /home/model-server/model-store

# Copy the model archive file to the container
COPY model-store/NER_BERT_Model.mar /home/model-server/model-store/
COPY config.properties /home/model-server/config.properties

WORKDIR /home/model-server/

# Install dependencies
COPY requirements.txt .
RUN pip install -U -r requirements.txt

CMD ["torchserve", \
     "--start", \
     "--model-store", "/home/model-server/model-store", \
     "--ts-config /home/model-server/config.properties", \
     "--models", \
     "NER_BERT_Model=NER_BERT_Model.mar"]