import logging
import torch
import os
import json
from transformers import AutoTokenizer, AutoModelForTokenClassification
from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)

class NERHandler(BaseHandler):
    tokenizer : AutoTokenizer = None
      
    def __init__(self, *args, **kwargs):
        logger.info("Loading NER model")
        super().__init__(*args, **kwargs)
        
    def initialize(self, context):
        """Initialize function loads the model and the tokenizer

        Args:
            context (context): It is a JSON Object containing information
            pertaining to the model artifacts parameters.

        Raises:
            RuntimeError: Raises the Runtime error when the model or
            tokenizer is missing

        """

        properties = context.system_properties
        self.manifest = context.manifest
        model_dir = properties.get("model_dir")

        # use GPU if available
        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else "cpu"
        )
        logger.info(f'Using device {self.device}')

        # load the model
        model_file = self.manifest['model']['modelFile']
        model_path = os.path.join(model_dir, model_file)

        if os.path.isfile(model_path):
            self.model = AutoModelForTokenClassification.from_pretrained(model_dir)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f'Successfully loaded model from {model_file}')
        else:
            raise RuntimeError('Missing the model file')

        # load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        if self.tokenizer is not None:
            logger.info('Successfully loaded tokenizer')
        else:
            raise RuntimeError('Missing tokenizer')

        # load mapping file
        mapping_file_path = os.path.join(model_dir, 'index_to_name.json')
        if os.path.isfile(mapping_file_path):
            with open(mapping_file_path) as f:
                self.mapping = json.load(f)
            logger.info('Successfully loaded mapping file')
        else:
            logger.warning('Mapping file is not detected')

        self.initialized = True
         
    def preprocess(self, requests):
        """Tokenize the input text using the suitable tokenizer and convert 
        it to tensor

        Args:
            requests: A list containing a dictionary, might be in the form
            of [{'body': json_file}] or [{'data': json_file}]
        """

        # unpack the data
        data = requests[0].get('body')
        if data is None:
            data = requests[0].get('data')

        texts = data.get('input')
        logger.info(f'Received {len(texts)} texts. Begin tokenizing')

        # tokenize the texts
        tokenized_data = self.tokenizer(texts,
                                        padding=True,
                                        return_tensors='pt')

        logger.info('Tokenization process completed')

        return tokenized_data
        
    def inference(self, inputs):
        """Predict class using the model

        Args:
            inputs: tensor of tokenized data
        """

        outputs = self.model(**inputs.to(self.device))
        predictions = torch.argmax(outputs.logits, dim=2)
        predictions = predictions.detach().cpu().numpy().tolist()
        logger.info('Inference completed')
        
        return predictions
    
    def postprocess(self, outputs: list, tokenized_data: dict):
        """
        Convert the output to the string label provided in the label mapper (index_to_name.json)

        Args:
            outputs (list): The integer label produced by the model

        Returns:
            List: The post process function returns a list of the predicted output.
        """
        data = self.tokenizer.batch_decode(tokenized_data['input_ids'])
        data = [text.split() for text in data]
        results = []
        for i, output in enumerate(outputs):
            predictions = [self.mapping[str(prediction)] for prediction in output]
            results_tuple = [(token, prediction) for token, prediction in zip(data[i], predictions) if token != '[PAD]' \
                or token != '[CLS]' or token != '[SEP]']
            logger.info(f'{results_tuple}')
            results.append(results_tuple)
        return [results]

    def handle(self, data, context):
        """
        This function handles the request to the model server
        """
        try:
            if not self.initialized:
                self.initialize(context)
            if data is None:
                return None
            tokenized_data = self.preprocess(data)
            outputs = self.inference(tokenized_data)
            results = self.postprocess(outputs, tokenized_data)
            return results
        except Exception as e:
            raise e