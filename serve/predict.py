import argparse
import json
import os
import pickle
import sys
import sagemaker_containers
import pandas as pd
import numpy as np

from sagemaker.predictor import csv_serializer

from utils import input_data_prep

def input_fn(serialized_input_data, content_type):
    print('Deserializing the input data.')
    if content_type == 'text/csv':
        data = serialized_input_data.decode('utf-8')
        return data
    raise Exception('Requested unsupported ContentType in content_type: ' + content_type)

def output_fn(prediction_output, accept):
    print('Serializing the generated output.')
    return str(prediction_output)

def predict_fn(input_data, estimator):
    
def predict_fn(data, estimator, content_type='text/csv'):
    """ Function to get predictions from numpy array."""
    # We need to tell the endpoint what format the data we are sending is in
    xgb_predictor.content_type = content_type
    xgb_predictor.serializer = csv_serializer
    
    Y_pred = xgb_predictor.predict(data).decode('utf-8')
    # predictions is currently a comma delimited string and so we would like to break it up
    # as a numpy array.
    predictions = np.fromstring(Y_pred, sep=',')
    
    return predictions
