import os

from flask import Flask, request, jsonify
import numpy as np

# Importe un module (module predict_client dans le package predict)
#import predict.predict_client as predict_client

# sur Gcloud Run, l'application main est lancée directement, sans référence au package. Le chemin du package ne fonctionne plus
#from predict import predict_client

# Avec __init__
#from predict import predict_client
#from predict import create_app  # Importe une fonction
#app = create_app()

# Sans __init__
import predict_package.predict_client as predict_client
#import predict_client
app = Flask(__name__)


@app.route("/liretxt")
def lire_txt():
    try:
        with open("test.txt", "r") as fichier:
            contenu = fichier.read()
            print(contenu)
            return f"Fichier test.txt : {contenu}"
    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
        return "Le fichier n'a pas été trouvé.", 404 # Retourner un code d'erreur HTTP
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return f"Une erreur est survenue : {e}", 500 # Retourner un code d'erreur HTTP

@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello OC-PJ7 {name}!"

@app.route("/predictbouchon")
def goto_predictbouchon():
    """Appel fonction predict"""
#    decision, score, seuil_decision = predict_client.predict_client_bouchon(None)
    decision, score, seuil_decision = predict_client.predict_client_bouchon(None)
    return jsonify({"decision": decision, "score": score, "seuil_decision": seuil_decision})

@app.route('/api/predict', methods=['POST'])
def APIpredict():
    try:
        # 1. Récupérer les données JSON de la requête
        data = request.get_json()

        # 2. Valider la présence des champs obligatoires
        if not data:
            return jsonify({'error': 'Aucune donnée fournie'}), 400  # 400 Bad Request

        required_fields = ['DAYS_BIRTH', 'CODE_GENDER_F', 'FLAG_RISKED_ORGANIZATION_TYPE',
                           'RATIO_INCOME_TO_FAM_MEMBERS', 'FLAG_STABLE_INCOME_TYPE',
                           'EXT_SOURCE_2',
                           'AMT_ALL_SUM_MEAN', 'RATIO_ALL_SUM_DEBT_TO_INCOME',
                           'RATIO_ALL_SUM_OVERDUE_TO_INCOME', 'RATIO_ALL_MAX_OVERDUE_TO_INCOME']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ "{field}" est obligatoire'}), 400

        # 3. Valider le format et valeurs autorisées des données
        try :
            # Tester les float
            float_fields = ['DAYS_BIRTH', 'RATIO_INCOME_TO_FAM_MEMBERS', 'EXT_SOURCE_2',
                               'AMT_ALL_SUM_MEAN', 'RATIO_ALL_SUM_DEBT_TO_INCOME',
                               'RATIO_ALL_SUM_OVERDUE_TO_INCOME', 'RATIO_ALL_MAX_OVERDUE_TO_INCOME']

            for field in float_fields:
                data[field] = float(data[field])  # Vérification format float
            
            # Test valeurs autorisées
            days_birth = data['DAYS_BIRTH']
            if days_birth > 0:
                raise ValueError(f'Uniquement valeurs < 0 autorisées pour DAYS_BIRTH : {days_birth}')

            # Tester les entier
            flag_fields = ['CODE_GENDER_F', 'FLAG_RISKED_ORGANIZATION_TYPE', 'FLAG_STABLE_INCOME_TYPE']
            for field in flag_fields:
                data[field] = int(data[field])  # Vérification format entier
                if data[field] not in [0, 1]:  # Valeurs autorisées
                    raise ValueError(f'Uniquement valeurs 0, 1 autorisées pour {field}')
             
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Erreur de type ou de format pour un des champs: {e}'}), 400
        
        # 4. Traitement des données
        X = np.array([data[field] for field in required_fields]) # Mets les données dans un array

        # Faire appel à predict
        decision, score, seuil_decision = predict_client.predict_Oneclient(X)
        resultat = {
            'decision': decision,
            'score': score,
            'seuil_decision': seuil_decision
        }

        # 5. Retourner une réponse JSON
        return jsonify(resultat), 200  # 200 OK

    except Exception as e:
        # Gestion des erreurs inattendues
        print(f"Erreur lors du traitement de la requête : {e}")  # Log de l'erreur pour le débogage
        return jsonify({'error': f'Une erreur inattendue s\'est produite : {e}'}), 500  # 500 Internal Server Error

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))  # Lance en local un serveur : http://localhost:8080/

