# Module des graphs utilisés par le Dashboard
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def graph_code_gender_f(axe, data):
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
