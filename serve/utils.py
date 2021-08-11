import numpy as np
import pandas as pd
from sklearn import preprocessing

def input_data_prep(df, person_id, offer_id, offer_type):
    """
    Creates a encoded np.array to input into the model to get predictions.
    """
    # Auxilars    
    input_values = np.array([])

    # Get person gender
    person_gender = df['gender'].unique()[0]

    values_list = [person_id, offer_id,  offer_type, person_gender]
    input_data = np.array(values_list).reshape((1,4))

    le_list = get_enconding_list(df)
    input_values = encode_input_data(input_data, le_list)
    
    return input_values


def get_enconding_list(df):

    columns_to_encoding = ['person', 'offer_id', 'offer_type', 'gender']
    le_list = []

    for i in columns_to_encoding:
        # Create an object LabelEncoder()
        le = preprocessing.LabelEncoder()
        # Get the list of values for the column
        values_to_encoding = df[i].values
        # Run the enconding for all possible values of the column
        le.fit(values_to_encoding)

        # Saves the Label Encoder Object to get inverse transform later
        le_list.append(le)

    return le_list

def encode_input_data(input_data, le_list):
    """Encode input data to input into Estimator endpoint."""
    encoded_list = []
    time_list = [0, 6, 12, 18]
    count = 0
    for i in range(0,4):
        le = le_list[i]
        df_input_values = pd.DataFrame(input_data).iloc[0, i:i+1].values
        encoded_list.append(le.transform(df_input_values))
    
    encoded_input = np.array(encoded_list).reshape((1,4))
    encoded_input = np.ones((4,1), dtype='int') * encoded_input
    encoded_input = np.insert(encoded_input, 0, 0, axis=1)

    for i in encoded_input:
        i[0] = time_list[count]
        count += 1
    
    return encoded_input