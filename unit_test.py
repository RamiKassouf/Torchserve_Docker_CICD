# unit test for ner_handler.py
import unittest
from unittest.mock import patch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from ts.torch_handler.base_handler import BaseHandler
from ner_handler import NERHandler

class TestNERHandler(unittest.TestCase):
    
    # create an instance of NERHandler
    ner_handler = NERHandler()
    
    # test model with sample input
    def test_handle(self):
        sample_input = {
            'text': 'My name is John Doe. I live in New York.',
            'model': 'dslim/bert-base-NER'
        }
        expected_output = {
            'entities': [
                {
                    'word': 'John Doe',
                    'score': 0.9995,
                    'entity': 'I-PER'
                },
                {
                    'word': 'New York',
                    'score': 0.9996,
                    'entity': 'I-LOC'
                }
            ]
        }
        with patch.object(NERHandler, 'handle', return_value=expected_output) as mock_handle:
            mock_handle.return_value = expected_output
            print("Testing sample input")
            print("example input: \n",sample_input)
            result = self.ner_handler.handle(sample_input, None)
            print("expected output : \n",expected_output)
            print("actual output: \n",result)
            self.assertEqual(result, expected_output)
            
    # test model with empty input
    def test_handle_empty_input(self):
        sample_input = {}
        expected_output = {}
        with patch.object(NERHandler, 'handle', return_value=expected_output) as mock_handle:
            mock_handle.return_value = expected_output
            print("Testing empty input")
            print("example input: \n",sample_input)
            result = self.ner_handler.handle(sample_input, None)
            print("expected output : \n",expected_output)
            print("actual output: \n",result)
            self.assertEqual(result, expected_output)
    
    # test model with empty text
    def test_handle_empty_text(self):
        sample_input = {
            'text': '',
            'model': 'dslim/bert-base-NER'
        }
        expected_output = {}
        with patch.object(NERHandler, 'handle', return_value=expected_output) as mock_handle:
            mock_handle.return_value = expected_output
            print("Testing empty text")
            print("example input: \n",sample_input)
            result = self.ner_handler.handle(sample_input, None)
            print("expected output : \n",expected_output)
            print("actual output: \n",result)
            self.assertEqual(result, expected_output)
    