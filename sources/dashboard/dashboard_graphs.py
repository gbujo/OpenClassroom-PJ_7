# Module des graphs utilisés par le Dashboard
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.colors import LinearSegmentedColormap, ListedColormap
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
    xmin = data[feature].quantile(0.05)
    xmax = data[feature].quantile(0.95)
    
    target_label = ['Client non risqué', 'Client à risque', 'Client en cours']  # Ajoute client en cours pour la légende
    
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

def graph_bivarie_marker(axe, data, features, feature_quali, feature_label, client_target, client_data, streamlit) :
    # Affiche un graph bi-varié
    # Ici feature, feature_label, feature_label sont des arrays de longeur 2 (pour les 2 variables)
    
    # Récupère les 2 features :
    feat1, feat2 = features
    
    # Limite min et max selon les quantiles (pour les 2 features)
    xmin = [data[feat].quantile(0.05) for feat in features]
    xmax = [data[feat].quantile(0.95) for feat in features]
    
    #target_label = ['Client non risqué', 'Client à risque', 'Client en cours']  # Ajoute client en cours pour la légende
    
    # Cut data selon les quantiles pour facilité la lecture du graph
    mask = (
        (data[feat1] >= xmin[0]) & (data[feat1] <= xmax[0])
           &
        (data[feat2] >= xmin[1]) & (data[feat2] <= xmax[1])
           )
    data_cut = data.loc[mask, [feat1, feat2, 'TARGET', 'y_pred_proba']]
    

    # Positionnement du client 
#    client_feature = client_data[feature].to_list()[0]

    fig = sns.relplot(
#        data=data_cut.loc[data_cut['TARGET'] == 1, :],
        data=data_cut.sample(5000, random_state=145),
        x=feat1, y=feat2,
        hue='y_pred_proba', style='TARGET', col='TARGET',
        palette=sns.diverging_palette(145, 20, s=60, as_cmap=True)
    )
#    fig.axes[0].set_ylabel('Proportion des clients', fontsize='small')


#    axe.set_xlabel(feature_label, fontsize='medium')
#    axe.set_ylabel('Proportion des clients', fontsize='small')
#    axe.set_title(feature_label, fontsize='medium')
#    axe.tick_params(axis='both', labelsize='small')
#    if client_feature < xmin : 
#        axe.axvline(xmin, c='b', ls='--')
#    elif client_feature > xmax :
#        axe.axvline(xmax, c='b', ls='--')
#        plt.arrow(0, xmax, 0.5, 0.5)
#    else :
#        axe.axvline(client_feature, c='b', ls='--')
#    axe.legend(target_label, fontsize='small')  # Bug avec legend produite par sns (ordre inversé)
#    plt.show()
        
    return fig

def graph_heatmap(axe, data, features, feature_quali, feature_label, client_target, client_data, seuil_decision, cbar) :
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
           )
    data_cut = data.loc[mask, [feat1, feat2, 'TARGET', 'y_pred_proba']]

    # Discretisation des features
    #
    df = pd.DataFrame()
    df['y_pred_proba'] = data_cut['y_pred_proba'].copy()
    df[f'{feat1}_BINS'], listbins_1 = pd.cut(data_cut[feat1], bins=10, labels=False, retbins=True)
    df[f'{feat2}_BINS'], listbins_2 = pd.cut(data_cut[feat2], bins=10, labels=False, retbins=True)    

    # Calcul du score moyen par cellule
    df_grouped = df.groupby([f'{feat1}_BINS', f'{feat2}_BINS'])[['y_pred_proba']].mean().reset_index()
    
    # Affichage dans Heatmap
    #
    # Mise en forme d'une pivot table pour la heatmap
    pivot_table = df_grouped.pivot(index=f'{feat1}_BINS', columns=f'{feat2}_BINS', values='y_pred_proba')
    # Trier l'index par ordre alphabétique décroissant
    pivot_table = pivot_table.sort_index(ascending=False)

    # Création Colomap centrée sur le seuil de décision
    seuil_decision = 0.3
    colors = ['darkgreen', 'lightgreen', 'mistyrose', 'red']  # CSS Colors
    nodes = [0.0, seuil_decision-0.05, seuil_decision, 1.0]
    cmap_seuil_decision = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))
    
    sns.heatmap(pivot_table, annot=True, fmt='.2f', cmap=cmap_seuil_decision,
                vmin=0, vmax=1,
               ax=axe, cbar=cbar)


    # Positionnement du client 
#    client_feature = client_data[feature].to_list()[0]



    axe.set_xlabel(feature_label[1], fontsize='medium')
    axe.set_ylabel(feature_label[0], fontsize='medium')
    axe.set_title('Carte des scores moyen des clients', fontsize='medium')
    axe.tick_params(axis='both', labelsize='x-small')
#    if client_feature < xmin : 
#        axe.axvline(xmin, c='b', ls='--')
#    elif client_feature > xmax :
#        axe.axvline(xmax, c='b', ls='--')
#        plt.arrow(0, xmax, 0.5, 0.5)
#    else :
#        axe.axvline(client_feature, c='b', ls='--')
#    axe.legend(target_label, fontsize='small')  # Bug avec legend produite par sns (ordre inversé)
        
    return axe
