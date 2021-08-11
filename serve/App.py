import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from serve.utils import input_data_prep
# from serve.predict import predict_fn
# importing the requests library
import requests

# Complete data to get all possible person ID and offers
df = pd.read_csv('transactions_people_offers.csv', sep=',')

# Title
st.markdown('# **Starbucks Capstone Project**')

# Get unique offer types
offer_types = df.offer_type.unique()
offer_type_selected = st.selectbox("Select the Offer type: ", offer_types)

# df = df.loc[(df.offer_type == offer_type_selected)].copy()

# Get unique offer ID
offer_ids = df.offer_id.unique()
offer_id_selected = st.selectbox("Select the Offer ID: ", offer_ids)

# df = df.loc[(df.offer_id == offer_id_selected)].copy()

# Get unique people ID
people_id = df.person.unique()
person_selected = st.selectbox("Select the Person ID: ", people_id)

# df = df.loc[(df.person == person_selected)].copy()

input_data = input_data_prep(df, person_selected, offer_id_selected, 
							offer_type_selected)

# defining the api-endpoint 
API_ENDPOINT = "https://xpfqnp3i55.execute-api.us-east-1.amazonaws.com/PROD"
print(person_selected, offer_id_selected,offer_type_selected)

if input_data[0][1] != 0:
    
	pd.DataFrame(input_data).to_csv('test_app.csv', sep=',', header=False, index=False)

	# sending post request and saving response as response object
	answer = requests.post(url = API_ENDPOINT, data = open('test_app.csv' ,'rb'))

	time_list = [0,6,12,18]
	answer = answer.content.decode()

	answer_list = []
	for i in answer.split(','):
	    answer_list.append(float(i))

	Y_pred = np.array(answer_list)

	
	print(Y_pred)

	np_to_plot = np.array([])
	np_to_plot = np.append(time_list, Y_pred)

	df_to_plot = pd.DataFrame(np_to_plot.reshape((2,4)).transpose())
	df_to_plot.rename(columns={0:'time', 1:'Predicted Transaction'}, inplace=True)

	fig = px.line(df_to_plot, x='time', y='Predicted Transaction', 
					title='Predicted Transactions by offer')
	# Show plot 
	st.plotly_chart(fig, use_container_width=True)

else:
	st.markdown('## No data to plot. Please, select a person and an offer.')


