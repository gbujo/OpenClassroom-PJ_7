import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import modules homemade
import dashboard_graphs  # dans le même répertoire

## Cas particullier predict qui pour l'instant n'est pas encore transformée en API
#import sys
#import os
## Obtenir le chemin absolu du répertoire contenant le module
#chemin_module = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "predict")) # Remonter d'un répertoire parent
# Ajouter le chemin au sys.path
#sys.path.append(chemin_module)
## Maintenant, vous pouvez importer le module
#import predict_client  # dans répertoire différent

import requests  # Pour call API prédiction

import pickle  # Pour lire les données SHAP

import logging

import shap



# Variables globales
#

@st.cache_data
def load_data():
    # Chemin d'accès aux datas
    data_path = 'https://storage.googleapis.com/bkjhd-sjhgsd-sq-iuoiu-iu-h-kjhkjh-jh/input'
    data = pd.read_csv(f'{data_path}/application_train_final_extract_20250212.csv')
    client_base =  pd.read_csv(f'{data_path}/application_test_final_extract_20250212.csv')
    client_base_shap = load_pickle(f'{data_path}/application_test_final_extract_shapvalues_20250212.pkl')
    return data, client_base, client_base_shap

@st.cache_data
def get_client(id_client, client_base, domain_features):
    """ Recherche les infos du client d'identifiant id_client
    Retourne ses données, ainsi que le rang du client dans le DataFrame (utilisé par la suite pour l'affichage des infos SHAP)
    """
    client_data = client_base.loc[client_base['SK_ID_CURR'] == id_client, domain_features]
    client_index = client_base.loc[client_base['SK_ID_CURR'] == id_client, :].index[0]
    client_rang = client_base.index.get_loc(client_index)
    return client_data, client_rang

@st.cache_data
def load_pickle(filename) :
    # filename : URL complete

    try:
        response = requests.get(filename, stream=True)  # stream=True pour les fichiers volumineux
        response.raise_for_status()  # Vérifier le code de statut HTTP (200 OK)  
        # Charger le fichier Pickle depuis le contenu téléchargé
        pickle_file = pickle.load(response.raw)
#        with open(filename, 'rb') as file:  # 'rb' for read binary
#            pickle_file = pickle.load(file)
#            st.write(pickle_file[0].data)
        print(f"Model loaded successfully from {filename}")  # Confirmation message
        # Écriture dans les journaux
        logging.info(f"Model loaded successfully from {filename}")
        return pickle_file
    except FileNotFoundError:
        print(f'Error: File not found at {filename}')
        logging.error(f'Error: File not found at {filename}')
        return None
    except pickle.UnpicklingError:
        print(f"Error: Could not unpickle the file at {filename}. It might be corrupted or created with a different pickle protocol.")
        logging.error(f"Error: Could not unpickle the file at {filename}. It might be corrupted or created with a different pickle protocol.")
        return None
    except Exception as e: # Catch other potential errors
        print(f"An unexpected error occurred: {e}")
        logging.error(f"An unexpected error occurred: {e}")
        return None
    return None

@st.cache_data
def get_prediction_oneclient(oneclient):
    """ Appel API prediction pour 1 client
    Input :
        - oneclient : dataframe pour 1 client
    Output :
        - client_decision [0,1]
        - client_score (sur 100)
        - seuil_decision (sur 100)
    """
    #url = "http://localhost:8080/api/predict"  # Serveur Flask local
    url = 'https://apipredict-1013078366791.europe-west9.run.app/api/predict'  # On GCP
    # Convertir en float et sous la forme d'un dictionnaire les données clients
    client_data = oneclient.astype(float).to_dict(orient='records')[0]
    response = requests.post(url, json=client_data)

    if response.status_code == 200:
        #print("Requête POST réussie")
        #print(response.text)
        #print("Contenu de la réponse :", response.json())
        client_decision, client_score, seuil_decision = *response.json().values(),
    else:
        st.write("Erreur lors de la requête POST")
        st.write("Code de statut :", response.status_code)
        st.write("Contenu de la réponse :", response.text)
        client_decision, client_score, seuil_decision = 1, 0, 99

    st.write(client_decision, client_score, seuil_decision)
   
    return client_decision, client_score, seuil_decision

# Afficher une jauge
#
import plotly.graph_objects as go

@st.cache_data
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
    return


def main():
    try:  
        # Sélection client
        #
        st.title('Credit approval dashboard')
    
        # Paramètres Features
        #

#        # Liste features
#        feature_domain=['DAYS_BIRTH', 'CODE_GENDER_F', 'FLAG_RISKED_ORGANIZATION_TYPE', 
#                 'RATIO_INCOME_TO_FAM_MEMBERS', 'FLAG_STABLE_INCOME_TYPE',
#                 'EXT_SOURCE_2',
#                 'AMT_ALL_SUM_MEAN', 'RATIO_ALL_SUM_DEBT_TO_INCOME', 'RATIO_ALL_SUM_OVERDUE_TO_INCOME',
#                 'RATIO_ALL_MAX_OVERDUE_TO_INCOME']

        # label des valeurs à afficher pour les features qualitatives
        feature_quali = {'CODE_GENDER_F': ['Autre genre','Genre féminin'],
                        'FLAG_RISKED_ORGANIZATION_TYPE': ['Autre organisation','Auto-entrepreneur'],
                        'FLAG_STABLE_INCOME_TYPE': ['Autre', 'Pension et retraite']}
        # Label à afficher pour les features
#        feature_label=['Age', 'Genre', 'Organisation professionelle', 'Revenus par membre du foyer', 'Stabilité revenus', 'Evaluation risque externe',
#                        'Montant moyen crédits passés', 'Ratio d\'endettement', 'Ratio défault de paiement', 'Ratio maximal défaut paiement mensuel']
        feature_label={'DAYS_BIRTH': 'Age',
                        'CODE_GENDER_F': 'Genre',
                        'FLAG_RISKED_ORGANIZATION_TYPE': 'Organisation professionelle', 
                        'RATIO_INCOME_TO_FAM_MEMBERS': 'Revenus par membre du foyer',
                        'FLAG_STABLE_INCOME_TYPE': 'Stabilité revenus',
                        'EXT_SOURCE_2': 'Evaluation risque externe',
                        'AMT_ALL_SUM_MEAN': 'Montant moyen crédits passés',
                        'RATIO_ALL_SUM_DEBT_TO_INCOME': 'Ratio d\'endettement',
                        'RATIO_ALL_SUM_OVERDUE_TO_INCOME': 'Ratio défaut de paiement',
                        'RATIO_ALL_MAX_OVERDUE_TO_INCOME': 'Ratio défaut paiement mensuel MAX'}
        feature_label_inverse = {valeur: cle for cle, valeur in feature_label.items()}  # Dictionnaire inversé pour retrouver le code avec le libellé
        feature_domain = list(feature_label.keys())

        # Load data
        #
        # Create a text element and let the reader know the data is loading.
        data_load_state = st.text('Loading data...')
        # Load data
        data, client_base, client_base_shap = load_data()
        # Notify the reader that the data was successfully loaded.
        data_load_state.text("")

        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(client_base)
        
        # Client courant
        #
        id_client = st.number_input(label='Numéro client :', value=None, format="%d", min_value=0, step=1, 
                                    placeholder='Renseigner un numéro de client')  # Input ID client
        if id_client is None :
            raise ValueError('Renseigner un numéro de client')
        if len(client_base.loc[client_base['SK_ID_CURR'] == id_client, :]) == 0 :
            raise ValueError('Numéro de client inconnu')
        client_data, client_rang = get_client(id_client, client_base, feature_domain)  # Recherche infos sur le client
        st.subheader('Client data :')
        client_data_affichage = client_data.copy()
        client_data_affichage.columns = list(feature_label.values())
        st.write(client_data_affichage.stack())  # Données du client dans Test
#        st.write(client_base_shap[client_rang].data)  # Données du client dans SHAP
#        st.write(client_rang)
               
        
        
        # Prédictions sur le client courant 
        #
        # Create a text element and let the reader know the score is being computed
        predict_state = st.text('Evaluation score client ...')

#        client_decision, client_score, seuil_decision = predict_client.predict_Oneclient(client_data.to_numpy())  # Transfo dataframe en array 1 dimension (10 features)
        client_decision, client_score, seuil_decision = get_prediction_oneclient(client_data)  # Appel API 

        # Notify the reader that the score was successfully computed
        predict_state.text("")
        
        st.subheader(f'Evaluation client : {"Client risqué" if client_decision == 1 else "Client non risqué"}')
#        st.write(predict_client.predict_Oneclient(client_data.to_numpy()))
        
        
        
        afficher_jauge(client_score, "Score risque client", seuil_decision, 0, 100)
        
        # Comparaison avec Autres clients
        #
        st.subheader('Positionnement du client :')
        feature_selected = st.multiselect(label='Selectionner 2 features à afficher :',
                                           options=list(feature_label.values()),
                                           max_selections=2,
                                          placeholder='Sélectionner 2 features à comparer')
        if len(feature_selected) != 2 :
            raise ValueError('Vous devez selectionner 2 features')
            
        feature1 = feature_label_inverse[feature_selected[0]]
        feature2 = feature_label_inverse[feature_selected[1]]
                     
        # Graphs pour les 2 features
        #
        fig, axs = plt.subplots(1,2, layout='constrained', figsize=[6, 3])

        # Choix du graph selon le type de features (quanti ou quali)
        for i, feat in enumerate([feature1, feature2]) :
            if feat in feature_quali :  # Feature de type qualitative
                _ = dashboard_graphs.graph_2categories(axs[i], data, feat, feature_quali[feat], feature_label[feat],
                                                         client_target=client_decision, client_data=client_data)
            else :
                _ = dashboard_graphs.graph_quantitatif(axs[i], data, feat, None, feature_label[feat],
                                                         client_target=client_decision, client_data=client_data)
        
        st.pyplot(fig)  # On passe directement l'objet figure

        # Grah bi-varié OLD
        #
        # fig = dashboard_graphs.graph_bivarie_marker(None, data, [feature1, feature2], None, None,
        #                                          client_target=client_decision, client_data=client_data, streamlit=st)
        # st.pyplot(fig)  # On passe directement l'objet figure

        # Heatmaps
        #
        st.write('Carte des scores moyen des clients')
        fig, axs = plt.subplots(1,2, layout='constrained', figsize=[6, 3])

        # Client non risqué
        _ = dashboard_graphs.graph_heatmap(axs[0], data.loc[data['TARGET'] == 0, :],
                                           [feature1, feature2],
                                           None, [feature_label[feature1], feature_label[feature2]],
                                           client_target=client_decision, client_data=client_data, seuil_decision=seuil_decision,
                                          cbar=False)
        axs[0].set_title('Clients non risqués', fontsize='medium')
        
        # Client risqué
        _ = dashboard_graphs.graph_heatmap(axs[1],  data.loc[data['TARGET'] == 1, :],
                                           [feature1, feature2],
                               None, [feature_label[feature1], feature_label[feature2]],
                               client_target=client_decision, client_data=client_data, seuil_decision=seuil_decision,
                                          cbar=True)
        axs[1].set_title('Clients à risque', fontsize='medium')

        st.pyplot(fig)  # On passe directement l'objet figure

        # Feature importance
        #
        st.subheader('Influence des données du client sur le score :')
        fig, ax = plt.subplots(1,1, layout='constrained')
        _ = dashboard_graphs.graph_feature_importance_global(ax, client_base_shap, client_rang)
        st.pyplot(fig)  # On passe directement l'objet figure
        fig, ax = plt.subplots(1,1, layout='constrained')
        _ = dashboard_graphs.graph_feature_importance_local(ax, client_base_shap, client_rang)
        st.pyplot(fig)  # On passe directement l'objet figure

    except ValueError as e:
        st.write(f'Error : {e}')
    
    return

# Code principal
#
if __name__ == "__main__":
    main()