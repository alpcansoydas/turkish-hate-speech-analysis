# -*- coding: utf-8 -*-
"""tr_hatespeech_model_usage.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pZcSzEop_2E8g3kL5H27zJTUIPMqM37Q
"""

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
import numpy as np
import warnings
from transformers import logging
logging.set_verbosity_error()
warnings.filterwarnings("ignore")

# Import pretrained tokenizer and model from https://huggingface.co/YSKartal/bert-base-turkish-cased-turkish_offensive_trained_model
tokenizer = AutoTokenizer.from_pretrained("YSKartal/bert-base-turkish-cased-turkish_offensive_trained_model")
bert = AutoModel.from_pretrained("YSKartal/bert-base-turkish-cased-turkish_offensive_trained_model",return_dict=False, from_tf=True)

class BERT_Arch(nn.Module):

    def __init__(self, bert):
      
      super(BERT_Arch, self).__init__()

      self.bert = bert 
      
      # dropout layer
      self.dropout = nn.Dropout(0.1)
      
      # relu activation function
      self.relu =  nn.ReLU()

      # dense layer 1
      self.fc1 = nn.Linear(768,512)

      # dense layer 3 (Output layer)
      self.fc3 = nn.Linear(512,2)

      #softmax activation function
      self.softmax = nn.LogSoftmax(dim=1)

    #define the forward pass
    def forward(self, sent_id, mask):

      #pass the inputs to the model  
      _, cls_hs = self.bert(sent_id, attention_mask=mask, return_dict=False)

      x = self.fc1(cls_hs)

      x = self.relu(x)

      x = self.dropout(x)

      # output layer
      x = self.fc3(x)

      # apply softmax activation
      x = self.softmax(x)

      return x

# pass the pre-trained Roberta to our define architecture
model = BERT_Arch(bert)

#load weights of the model
path = 'turkish_offensive_language.pt'
model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))

# Define predict function (2=>POSITIVE 1=>NEGATIVE 0=>NEUTRAL)
def predict_sentiment(text):
  tokenized = tokenizer.encode_plus(
    text,
    pad_to_max_length=True,
    truncation=True,
    return_token_type_ids=False
    )

  input_ids = tokenized['input_ids']
  attention_mask = tokenized['attention_mask']

  seq = torch.tensor(input_ids)
  mask = torch.tensor(attention_mask)
  seq = seq.unsqueeze(0)
  mask = mask.unsqueeze(0)
  preds = model(seq, mask)
  preds = preds.detach().cpu().numpy()
  result = np.argmax(preds, axis=1)
  preds = torch.tensor(preds)
  probabilities = nn.functional.softmax(preds)

  return {'OFFENSIVE':float(probabilities[0][1]),
          'NOT OFFENSIVE':float(probabilities[0][0])}

predict_sentiment('Çok aptal bir sisteminiz var.')