# Module des graphs utilisés par le Dashboard
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import copy


def graph_2categories(axe, data, feature, feature_quali, feature_label, client_target, client_data) :

    target_label = ['Client non risqué', 'Client à risque']
    
    feature_quali.append('Client en cours') # Pour la légende, on ajoute le client en cours
    client_feature = client_data[feature].to_list()[0]

    
    # Proportions des clients selon la target (colonne) et par genre (ligne)
    proportions = data.groupby(['TARGET', feature])[feature].count() / data.groupby('TARGET')[feature].count()
    proportions = proportions.unstack().transpose().to_numpy()*100
    
    # Positionnement du client 
    pos_client = np.zeros(2*2).reshape(2,2)
    pos_client[client_feature, client_target] = 1
    pos_client = pos_client * proportions  # On ne garde que la valeur Target et Genre correspondant au client
    
    bottom = np.zeros(2)
    pos_client_bottom = np.zeros(2)
    for i, ligne in enumerate(proportions) :
        p = axe.bar([0.25, 0.75], ligne, width=0.25, bottom=bottom)
        if i == client_feature :
            pos_client_bottom = copy.deepcopy(bottom)  # On conserve la base pour pouvoir afficher la cellule du client après
        bottom += ligne
        axe.bar_label(p, label_type='center', fmt='%.1f%%')
    axe.bar([0.25, 0.75], pos_client[client_feature], width=0.25, bottom=pos_client_bottom,
           color='none', edgecolor='b', facecolor='none', linestyle='--', linewidth=2.0)

    axe.set_xlabel('Risque client', fontsize='medium')
    axe.set_ylabel('Proportion des clients', fontsize='small')
    axe.set_title(feature_label, fontsize='medium')
    axe.set_xticks([0.25, 0.75], target_label, fontsize='small')
    axe.tick_params(axis='both', labelsize='small')
    axe.set_xlim([0, 1])
    axe.legend(feature_quali, fontsize='small')
    plt.show()
    
    return axe


    
def graph_qualitatif(axe, data, feature, feature_quali, feature_label, client_target, client_data) :
    # Limite min et max selon les quantiles
    xmin = data[feature].quantile(0.10)
    xmax = data[feature].quantile(0.90)
    
    target_label = ['Client non risqué', 'Client à risque', 'Client en cours']  # Ajoute client en cours pour la légende
    
    # Construction serie 2D : data pour les deux valeurs de TARGET
#    data_grouped = data.groupby('TARGET')[feature]
    data_grouped = data.loc[(data[feature] >= xmin) & (data[feature] <= xmax)].groupby('TARGET')[feature]
    serie=[]
    for name, group in data_grouped:
        serie.append(group.to_list())

    # Positionnement du client 
    client_feature = client_data[feature].to_list()[0]

#    axe.hist(serie, bins=100, density=True, label=target_label, color=['g', 'r'], histtype='step')
    sns.kdeplot(data, x=feature, hue='TARGET', common_norm=False, ax=axe, palette=['g', 'r'])
    
    axe.set_xlabel(feature_label, fontsize='medium')
    axe.set_ylabel('Proportion des clients', fontsize='small')
    axe.set_title(feature_label, fontsize='medium')
    axe.tick_params(axis='both', labelsize='small')
    if client_feature < xmin : 
        axe.axvline(xmin, c='b', ls='--')
    elif client_feature > xmax :
        axe.axvline(xmax, c='b', ls='--')
        plt.arrow(0, xmax, 0.5, 0.5)
    else :
        axe.axvline(client_feature, c='b', ls='--')
    axe.legend(target_label, fontsize='small')  
    plt.show()

    return axe
