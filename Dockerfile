FROM pytorch/torchserve:latest-cpu


# Create the directories for the model store and the NER BERT Model
RUN mkdir -p model-store NER_BERT_Model

# copy the model files to the container
COPY ner_handler.py index_to_name.json  /home/model-server/
COPY special_tokens_map.json tokenizer_config.json config.json tokenizer.json vocab.txt  pytorch_model.bin /home/model-server/NER_BERT_Model/
COPY requirements.txt /home/model-server/


#Install dependencies
RUN pip install -U -r /home/model-server/requirements.txt

WORKDIR /home/model-server/

# Create the model archive
RUN torch-model-archiver \
  --model-name=NER_BERT_Model \
  --version=1.0 \
  --model-file=NER_BERT_Model/pytorch_model.bin \
  --handler=/home/model-server/ner_handler.py \
  --extra-files=NER_BERT_Model/config.json,index_to_name.json,NER_BERT_Model/special_tokens_map.json,\
                NER_BERT_Model/tokenizer_config.json,NER_BERT_Model/tokenizer.json \
  --export-path=model-store

CMD ["torchserve", \
     "--start", \
     "--model-store", "/home/model-server/model-store", \
     "--ts-config /home/model-server/config.properties", \
     "--models", \
     "NER_BERT_Model=NER_BERT_Model.mar"]