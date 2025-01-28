# Module des graphs utilisés par le Dashboard
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def init_graphs():
# Créer un dictionnaire avec titre et légende à afficher selon la feature
    dict_labels = {
        
    }
    return dict_labels

def graph_code_gender_f_OLD(axe, data):
    feature = 'CODE_GENDER_F'
    mask = data['TARGET'] == 1
    axe.hist([data.loc[mask, feature], data.loc[~mask, feature]], bins=2, density=True, histtype='bar', 
            label=['Client risqué', 'Client non risqué'],
           color=['r', 'g'])
    axe.set_xlabel('Genre du client')
    axe.set_ylabel('Proportion des clients')
    axe.set_title('Donnée : Genre du client')
    axe.set_xticks([0.25, 0.75], ['Autres', 'Féminin'])
    axe.legend()    
    return axe


def graph_code_gender_f(axe, data):
    feature = 'CODE_GENDER_F'
    proportions = data.groupby(['TARGET', feature])[feature].count() / data.groupby('TARGET')[feature].count()
    proportions = proportions.unstack().to_numpy().transpose()*100
    
    feature_label = ['Autre genre','Genre féminin']
    target_label = ['Client non risqué', 'Cient à risque']
    
#    fig, ax = plt.subplots()
    bottom = np.zeros(2)
    for ligne in proportions :
        p = axe.bar([0.25, 0.75], ligne, width=0.25, bottom=bottom)
        bottom += ligne
        axe.bar_label(p, label_type='center', fmt='%.1f%%')
    axe.set_xlabel('Risque client')
    axe.set_ylabel('Proportion des clients (%)')
    axe.set_title('Proportion du risque client par genre')
    axe.set_xticks([0.25, 0.75], target_label)
    axe.set_xlim([0, 1])
    axe.legend(feature_label)
    plt.show()
    return axe

def graph_2categories(axe, data, feature, feature_label, client_target, client_data) :
    import copy
    
#    client_target = 0
#    client_code_gender_f = 1
    
#    feature_label = ['Autre genre','Genre féminin', 'Client en cours']
    client_feature = client_data[feature].to_list()[0]
    target_label = ['Client non risqué', 'Client à risque']
    
    # Proportions des clients selon la target (colonne) et par genre (ligne)
    proportions = data.groupby(['TARGET', feature])[feature].count() / data.groupby('TARGET')[feature].count()
    proportions = proportions.unstack().transpose().to_numpy()*100
    
    # Positionnement du client 
    pos_client = np.zeros(2*2).reshape(2,2)
    pos_client[client_feature, client_target] = 1
    pos_client = pos_client * proportions  # On ne garde que la valeur Target et Genre correspondant au client
    
#    fig, ax = plt.subplots()
    bottom = np.zeros(2)
    pos_client_bottom = np.zeros(2)
    for i, ligne in enumerate(proportions) :
        p = axe.bar([0.25, 0.75], ligne, width=0.25, bottom=bottom)
        if i == client_feature :
            pos_client_bottom = copy.deepcopy(bottom)  # On conserve la base pour pouvoir afficher la cellule du client après
        bottom += ligne
        axe.bar_label(p, label_type='center', fmt='%.1f%%')
    #ax.bar([0.25, 0.75], pos_client[client_code_gender_f], width=0.25, bottom=pos_client_bottom,
    #       color=None, linestyle='--', linewidth=3)
    axe.bar([0.25, 0.75], pos_client[client_feature], width=0.25, bottom=pos_client_bottom,
           color='none', edgecolor='g', facecolor='none', linestyle='--', linewidth=2.0)
    axe.set_xlabel('Risque client')
    axe.set_ylabel('Proportion des clients (%)')
    axe.set_title('Répartition des risques client')
    axe.set_xticks([0.25, 0.75], target_label)
    axe.set_xlim([0, 1])
    axe.legend(feature_label)
    plt.show()
    
    return axe