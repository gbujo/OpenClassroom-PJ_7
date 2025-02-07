# API prédiction client
import numpy as np
import pickle  # Fait parti de Python

# Pour accèder au modèle
import sys
import os

def load_model(filepath):
    """Loads a pickled model from the specified filepath.

    Args:
        filepath: The path to the .pkl file.

    Returns:
        The loaded model object, or None if an error occurs.
        Prints an error message to the console in case of failure.
    """
    try:
        with open(filepath, 'rb') as file:  # 'rb' for read binary
            model = pickle.load(file)
        print(f"Model loaded successfully from {filepath}")  # Confirmation message
        return model
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except pickle.UnpicklingError:
        print(f"Error: Could not unpickle the file at {filepath}. It might be corrupted or created with a different pickle protocol.")
        return None
    except Exception as e: # Catch other potential errors
        print(f"An unexpected error occurred: {e}")
        return None

def predict_client_bouchon(X):
    # Mode bouchon
    decision = 0
    score = 1.0
    seuil_decision = 99.9
    return decision, score, seuil_decision

def predict_client(X) :
    """ Prédiction pour n clients
       Input :
            X : array n features for n clients (2 dimensions)
    """

    # Load model
    # Indique le chemin absolu du répertoire contenant le module
#    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')) 
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model.pkl'))  # Model se trouve dans le meme répertoire
#    loaded_model = load_model(model_path)
    loaded_model = pickle.load('https://storage.googleapis.com/bkjhd-sjhgsd-sq-iuoiu-iu-h-kjhkjh-jh/model/model.pkl')
    
    if loaded_model:
        # Now you can use the loaded model
        print(type(loaded_model)) # Print the type of the model for verification
        decision = loaded_model.predict(X)
        score = loaded_model.predict_proba(X)
        seuil_decision = loaded_model.best_threshold_
    else:
        print("Model loading failed.")
        return 1, 1, 1
    
#    return decision, score, seuil_decision pour 1 seul client
#    return decision[0], score[0,1], seuil_decision
    return decision, score, seuil_decision

def predict_Oneclient(X) :
    """ Prédiction pour 1 client
       Input :
            X : array n features for 1 client (1 dimension)
    """

    # Load model
    # Indique le chemin absolu du répertoire contenant le module
#    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')) 
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model.pkl'))  # model dans le meme répertoire (c est plus simple)
    loaded_model = load_model(model_path)
    
    if loaded_model:
        # Now you can use the loaded model
        print(type(loaded_model)) # Print the type of the model for verification
        X = X.reshape(1, -1)  # Nécessité de remettre à 2D pour predict et predict_proba
        decision = loaded_model.predict(X)
        score = loaded_model.predict_proba(X)
        seuil_decision = loaded_model.best_threshold_
    else:
        print("Model loading failed.")
        return 1, 1, 1
    
#    return decision, score, seuil_decision pour 1 seul client
#    return decision[0], score[0,1], seuil_decision
    return int(decision[0]), score[0,1]*100, seuil_decision*100