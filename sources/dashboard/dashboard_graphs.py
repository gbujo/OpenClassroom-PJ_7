# Module des graphs utilisés par le Dashboard
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import copy

import shap

import streamlit as st


def graph_2categories(axe, data, feature, feature_quali, feature_label, client_target, client_data) :

    target_label = ['Clients non risqués', 'Clients à risque']
    
    feature_quali.append('Client en cours') # Pour la légende, on ajoute le client en cours
    client_feature = client_data[feature].to_list()[0]

    
    # Proportions des clients selon la target (colonne) et par genre (ligne)
    proportions = data.groupby(['TARGET', feature])[feature].count() / data.groupby('TARGET')[feature].count()
    proportions = proportions.unstack().transpose().to_numpy()*100
    
    # Positionnement du client 
    pos_client = np.zeros(2*2).reshape(2,2)
#    pos_client[client_feature, client_target] = 1
    pos_client[client_feature, :] = 1
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


    
def graph_quantitatif(axe, data, feature, feature_quali, feature_label, client_target, client_data) :
    # Limite min et max selon les quantiles
    xmin = data[feature].quantile(0.05)
    xmax = data[feature].quantile(0.95)
    
    target_label = ['Clients non risqués', 'Clients à risque', 'Client en cours']  # Ajoute client en cours pour la légende
    
    # Construction serie 2D : data pour les deux valeurs de TARGET
#    data_grouped = data.groupby('TARGET')[feature]
    data_grouped = data.loc[((data[feature] >= xmin) & (data[feature] <= xmax)), :].groupby('TARGET')[feature]
#    serie=[]
#    for name, group in data_grouped:
#        serie.append(group.to_list())

    # Positionnement du client 
    client_feature = client_data[feature].to_list()[0]

#    axe.hist(serie, bins=100, density=True, label=target_label, color=['g', 'r'], histtype='step')
    sns.kdeplot(data.loc[((data[feature] >= xmin) & (data[feature] <= xmax)), :],
                x=feature, hue='TARGET', common_norm=False, ax=axe, palette=['g', 'r'], cut=0)
    
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
#    axe.legend(target_label, fontsize='small')  # Bug avec legend produite par sns (ordre inversé)
    plt.show()

    return axe


def graph_heatmap(axe, data, target, features, feature_quali, feature_label, client_target, client_data, seuil_decision, cbar) :
    # Affiche une heatmap avec la color map centrée sur le seuil de décision
    # Ici feature, feature_label, feature_label sont des arrays de longeur 2 (pour les 2 variables)
    
    # Récupère les 2 features :
    feat1, feat2 = features

    # Cut data selon les quantiles pour facilité la lecture du graph
    #
    # Limite min et max selon les quantiles (pour les 2 features)
    xmin = [data[feat].quantile(0.05) for feat in features]
    xmax = [data[feat].quantile(0.95) for feat in features]
    mask = (
        (data[feat1] >= xmin[0]) & (data[feat1] <= xmax[0])
           &
        (data[feat2] >= xmin[1]) & (data[feat2] <= xmax[1])
           &
        (data['TARGET'] == target)
        )
    data_cut = data.loc[mask, [feat1, feat2, 'TARGET', 'y_pred_proba']]

    # Discretisation des features
    #
    nbins = 10  # Nombre de bins
    list_bins=[]  # Liste des bins pour chaque feature
    df = pd.DataFrame()
    df['y_pred_proba'] = data_cut['y_pred_proba'].copy()
    for feat in features :
        df[f'{feat}_BINS'], retbins = pd.cut(data_cut[feat], bins=nbins, labels=False, retbins=True)
        list_bins.append(retbins)

#    # Calcul du score moyen par cellule
    pivot_table = df.pivot_table(index=f'{feat1}_BINS', columns=f'{feat2}_BINS', values='y_pred_proba', aggfunc='mean')
    # Ajouter colonnes vides avec des valeurs vides
    for i in range(nbins):
        if i not in pivot_table.columns :
            pivot_table.loc[:, i] = np.nan
        if i not in pivot_table.index.to_list() :
            pivot_table.loc[i, :] = np.nan
    
    # Trier index et colonnes par ordre alphabétique décroissant
    pivot_table = pivot_table.sort_index(axis= 0, ascending=False)  # Trie lignes
    pivot_table = pivot_table.sort_index(axis= 1, ascending=True)  # Trie colonnes
    
    # Création Colomap centrée sur le seuil de décision
    seuil_decision = seuil_decision / 100.0  # color map entre 0 et 1
    colors = ['darkgreen', 'lightgreen', 'mistyrose', 'red']  # CSS Colors
    nodes = [0.0, seuil_decision-0.05, seuil_decision, 1.0]
    cmap_seuil_decision = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
    
    sns.heatmap(pivot_table, annot=False, fmt='.2f', cmap=cmap_seuil_decision,
                vmin=0, vmax=1,
               ax=axe, cbar=cbar)

    # Positionnement du client 
    X = client_data[features].to_numpy()[0].tolist()  # Les 2 valeurs des features pour le client
    # Revenir entre [xmin,xmax] si on est au-delà
    X = [valeur_dans_intervalle(val, val_min, val_max) for val, val_min, val_max in zip(X, xmin, xmax)]
    # Recherche du rang du bin pour chaque feature
    Xbin = []
    for f in range(2):
        isel=0
        for i in range(nbins):
            if X[f] > list_bins[f][i] and X[f] <= list_bins[f][i+1] :
                isel=i
        Xbin.append(isel)

    axe.plot([Xbin[1]+0.5], [nbins-Xbin[0]-0.5], marker='*', c='b')

    # Set-up graphs
    axe.set_xlabel(feature_label[1], fontsize='medium')
    axe.set_ylabel(feature_label[0], fontsize='medium')
    axe.set_title('Carte des scores moyen des clients', fontsize='medium')
    axe.tick_params(axis='both', labelsize='x-small')
       
    return axe

def valeur_dans_intervalle(val, val_min, val_max):
  """
  Retourne la valeur de val si elle se trouve dans l'intervalle [val_min, val_max],
  sinon retourne la borne la plus proche de l'intervalle.
  """
  if val_min <= val <= val_max:
    return val
  elif val < val_min:
    return val_min
  else:
    return val_max


def graph_feature_importance_setup(axe, title):
    axe.tick_params(axis='both', labelsize='small')
    axe.set_xlabel(axe.get_xlabel(), fontsize='small')
    # Récupérer les objets texte (annotations)
    texts = [child for child in axe.get_children() if isinstance(child, plt.Text)]
    # Modifier la taille du texte pour chaque annotation
    for text in texts:
        text.set_size('small')    
    axe.set_title(title, fontsize='large')
    return axe

def graph_feature_importance_global(axe, shap_values, rang):
    shap.plots.bar(shap_values, ax=axe)
    axe = graph_feature_importance_setup(axe, 'Feature importance globale')
    return axe

def graph_feature_importance_local(axe, shap_values, rang):
    shap.plots.bar(shap_values[rang], ax=axe)
    axe = graph_feature_importance_setup(axe, 'Feature importance locale')
    return axe

