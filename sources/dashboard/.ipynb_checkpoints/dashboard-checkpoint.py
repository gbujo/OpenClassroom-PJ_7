import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import modules homemade
import dashboard_graphs  # dans le même répertoire

# Cas particullier predict qui pour l'instant n'est pas encore transformée en API
import sys
import os
# Obtenir le chemin absolu du répertoire contenant le module
chemin_module = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "predict")) # Remonter d'un répertoire parent
# Ajouter le chemin au sys.path
sys.path.append(chemin_module)
# Maintenant, vous pouvez importer le module
import predict_client  # dans répertoire différent


st.title('Credit approval dashboard')


# Accès aux data
#
data_path = 'c:/users/innov/python_venv/oc-pj7/input'
@st.cache_data
def load_data():
#    data = pd.read_csv(f'{data_path}/application_train_20250103.csv', nrows=10000)
    data = pd.read_csv(f'{data_path}/application_train_20250103.csv', nrows=10000)
    data = data.iloc[:, 3:]  # Je supprime des colonnes de réplication des index (je ne sais pas d'où elles viennent mais pas grave)
#    client_base =  pd.read_csv(f'{data_path}/application_test_20250103.csv', nrows=1000)
    client_base =  pd.read_csv(f'{data_path}/application_test_20250103.csv', nrows=1000)
    client_base = client_base.iloc[:, 3:]  # Je supprime des colonnes de réplication des index (je ne sais pas d'où elles viennent mais pas grave)
    return data, client_base

@st.cache_data
def load_client(id_client):
    domain_features=['DAYS_BIRTH', 'CODE_GENDER_F', 'FLAG_RISKED_ORGANIZATION_TYPE', 
                     'RATIO_INCOME_TO_FAM_MEMBERS', 'FLAG_STABLE_INCOME_TYPE',
                     'EXT_SOURCE_2',
                     'AMT_ALL_SUM_MEAN', 'RATIO_ALL_SUM_DEBT_TO_INCOME', 'RATIO_ALL_SUM_OVERDUE_TO_INCOME',
                     'RATIO_ALL_MAX_OVERDUE_TO_INCOME']
#    client_data = client_base.loc[client_base['SK_ID_CURR'] == id_client, domain_features].stack()
    client_data = client_base.loc[client_base['SK_ID_CURR'] == id_client, domain_features]
    return client_data


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
    st.write(client_base)

# Client courant
#
id_client = st.number_input('Numéro client :', value=None, format="%d", min_value=0, step=1)  # Input ID client
client_data = load_client(id_client)  # Recherche infos sur le client
st.subheader('Client data :')
st.write(client_data.stack())


# Prédictions sur le client courant :
client_decision, client_score, seuil_decision = predict_client.predict_client(client_data.to_numpy().reshape(1, -1))  # Transfo dataframe en array 2 dimensions (10 features, 1 sample)
client_score = client_score*100
seuil_decision = seuil_decision*100
st.subheader(f'Evaluation client : {"Client risqué" if client_decision == 1 else "Client non risqué"}')
st.write(predict_client.predict_client(client_data.to_numpy().reshape(1, -1)))


# Afficher une jauge
#
import plotly.graph_objects as go

def afficher_jauge(valeur, titre, seuil, min_val=0, max_val=100):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = valeur,
        title = {'text': titre},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "darkblue"}, # Couleur de la barre
            'steps' : [
                {'range': [min_val, seuil], 'color': "green"}, # Zones de couleur
#                {'range': [max_val/3, 2*max_val/3], 'color': "orange"},
                {'range': [seuil, max_val], 'color': "red"}],
            'threshold' : {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': seuil} # Seuil avec une ligne
        }
    ))
    st.plotly_chart(fig)

afficher_jauge(client_score, "Score risque client", seuil_decision, 0, 100)

# Autres clients
#
st.subheader('Positionnement du client :')

#  A FAIRE
# dict_graph = dashboard_graphs.init_graph()

# Affichage du graphique dans Streamlit
fig, axs = plt.subplots(1,2, layout='constrained')
_ = dashboard_graphs.graph_2categories(axs[0], data, 'CODE_GENDER_F', ['Autre genre','Genre féminin', 'Client en cours'],
                                         client_target=client_decision, client_data=client_data)
_ = dashboard_graphs.graph_2categories(axs[1], data, 'FLAG_RISKED_ORGANIZATION_TYPE', ['Autre organisation','Auto-entrepreneur', 'Client en cours'],
                                         client_target=client_decision, client_data=client_data)

st.pyplot(fig)  # On passe directement l'objet figure