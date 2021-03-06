"""Tests for the ArgBiLSTM model"""

import numpy
import unittest

from models.arg_bilstm import ArgBiLSTM
from models.att_arg_bilstm import TimePreAttArgBiLSTM, FeaturePreAttArgBiLSTM


class ArgBiLSTMTest(unittest.TestCase):
    """Tests for the ArgBiLSTM model"""
    MODEL = ArgBiLSTM

    def setUp(self):
        self.batch_size = 10
        self.embedding_size = 5
        vocab_size = 12
        embeddings = numpy.random.rand(vocab_size, self.embedding_size)
        mappings = {
            'tokens': {'hello': 1, 'world': 2, 'it': 3, 'is': 5, 'nice': 4,
                       'a': 6, 'day': 7},
            'labels': {'0': 0, '1': 1, '2': 2},
            'casing': {
                'PADDING': 0, 'allLower': 4, 'allUpper': 5, 'contains_digit': 7,
                'initialUpper': 6, 'mainly_numeric': 3, 'numeric': 2,
                'other': 1
            }
        }
        self.data = {'name' : {
            'trainMatrix': [{
                    'labels': [0, 0],
                    'raw_tokens': ['hello', 'world'],
                    'tokens': [1, 2],
                    'casing': [5, 4]
                },{
                    'labels': [0, 0, 1, 1, 1],
                    'raw_tokens': ['it', 'is', 'a', 'nice', 'day'],
                    'tokens': [3, 5, 6, 4, 7],
                    'casing': [4, 4, 4, 4, 4]
                },{
                    'labels': [0, 0],
                    'raw_tokens': ['PADDING', 'world'],
                    'tokens': [0, 2],
                    'casing': [0, 4]  # We have a padding token?
                }
            ],
            'devMatrix': [{
                    'labels': [1, 1, 0, 0],
                    'raw_tokens': ['nice', 'day', 'it', 'is'],
                    'tokens': [4, 7, 3, 5],
                    'casing': [4, 4, 4, 4]
                }],
            'testMatrix': [{
                    'labels': [1, 1, 0, 0],
                    'raw_tokens': ['nice', 'day', 'it', 'is'],
                    'tokens': [4, 7, 3, 5],
                    'casing': [4, 4, 4, 4]
                }]
        }}
        datasets = {'name': {
            'columns': {},  # Not necessary for test
            'commentSymbol': None,  # Not necessary for test
            'dirpath': '',  # Not necessary for test
            'evaluate': True,
            'label': 'labels'
        }}
        classifier_params = {
            'charEmbeddingsSize': None,
            'charEmbeddings': None
        }
        self.model = self.MODEL(classifier_params)
        self.model.setMappings(mappings, embeddings)
        self.model.setDataset(datasets, self.data)

    def test_build(self):
        """Test the model can be successfully built"""
        self.model.buildModel()

    def test_fit(self):
        """Test the model can be fitted"""
        self.model.fit(epochs=2)

    def test_tag_sentences(self):
        """Test if the model can tag sentences."""
        self.model.buildModel()
        sentences = self.data['name']['trainMatrix']
        predicted_labels = self.model.tagSentences(sentences)
        self.assertEqual(len(sentences), len(predicted_labels['name']))
        for true, predicted in zip(sentences, predicted_labels):
            self.assertEqual(numpy.asarray(true).shape,
                             numpy.asarray(predicted).shape)


class AttArgBiLSTMTest(ArgBiLSTMTest):
    MODEL = TimePreAttArgBiLSTM

    def test_predict(self):
        """Test the model can be fitted"""
        self.model.fit(epochs=1)
        labels = self.model.predict(self.data['name']['trainMatrix'])
        for sentence_label, sentence in zip(
                labels['name'], self.data['name']['trainMatrix']):
            no_pad_tokens = len([x for x in sentence['tokens'] if x != 0])
            self.assertEqual(no_pad_tokens, len(sentence_label))

    def test_predict_attention(self):
        """Test the model can be fitted"""
        self.model.fit(epochs=1)
        labels, attention = self.model.predict(self.data['name']['trainMatrix'],
                                    return_attention=True)
        for sentence_attention, sentence in zip(
                attention['name'], self.data['name']['trainMatrix']):
            no_pad_tokens = len([x for x in sentence['tokens'] if x != 0])
            self.assertEqual(no_pad_tokens, len(sentence_attention))


class FeaturePreAttArgBiLSTMTest(AttArgBiLSTMTest):
    MODEL = FeaturePreAttArgBiLSTM


if __name__ == '__main__':
    unittest.main()
