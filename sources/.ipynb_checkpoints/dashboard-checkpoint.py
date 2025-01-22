import streamlit as st
import pandas as pd
import numpy as np

st.title('Credit approval dashboard')

@st.cache_data
def load_data():
    data = pd.read_csv('../data/application_train_features.csv', nrows=10000)
    data = data.iloc[:, 3:]  # Je supprime des colonnes de réplication des index (je ne sais pas d'où elles viennent mais pas grave)
    client_base =  pd.read_csv('../data/application_test_features.csv', nrows=1000)
    client_base = client_base.iloc[:, 3:]  # Je supprime des colonnes de réplication des index (je ne sais pas d'où elles viennent mais pas grave)
    return data, client_base

@st.cache_data
def load_client(id_client):
    domain_features=['DAYS_BIRTH', 'CODE_GENDER_F', 'FLAG_RISKED_ORGANIZATION_TYPE', 
                     'RATIO_INCOME_TO_FAM_MEMBERS', 'FLAG_STABLE_INCOME_TYPE',
                     'EXT_SOURCE_2',
                     'AMT_ALL_SUM_MEAN', 'RATIO_ALL_SUM_DEBT_TO_INCOME', 'RATIO_ALL_SUM_OVERDUE_TO_INCOME',
                     'RATIO_ALL_MAX_OVERDUE_TO_INCOME']
    client_data = client_base.loc[client_base['SK_ID_CURR'] == id_client, domain_features].stack()
    return client_data

@st.cache_data
def predict_client(id_client):
    # Mode bouchon
    target = 1
    score = 0.7
    return target, score


# Load data
#
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load data
data, client_base = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Client courant
#
id_client = st.number_input('Numéro client :', value=None, format="%d", min_value=0, step=1)  # Input ID client
client_data = load_client(id_client)  # Recherche infos sur le client
st.subheader('Client data :')
st.write(client_data)

client_target, client_score = predict_client(id_client)  # Recherche prédictions
st.subheader('Client scoring :')
st.write(client_target, client_score)


