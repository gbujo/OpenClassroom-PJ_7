# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_helloworld_service]
import os

from flask import Flask, request, jsonify
import numpy as np



import predict_client

app = Flask(__name__)

@app.route("/liretxt")
def lire_txt():
    try:
        with open("test.txt", "r") as fichier:
            contenu = fichier.read()
            print(contenu)
    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    return f"Fichier test.txt {contenu}!"


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello OC-PJ7 {name}!"

@app.route("/predictbouchon")
def goto_predictbouchon():
    """Appel fonction predict"""
    decision, score, seuil_decision = predict_client.predict_client_bouchon(None)
    return f"Voici les prédictions bouchons {decision, score, seuil_decision}"

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
                 'AMT_ALL_SUM_MEAN', 'RATIO_ALL_SUM_DEBT_TO_INCOME', 'RATIO_ALL_SUM_OVERDUE_TO_INCOME', 'RATIO_ALL_MAX_OVERDUE_TO_INCOME']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ "{field}" est obligatoire'}), 400

        # 3. Valider le format des données
        days_birth = data['DAYS_BIRTH']
        if not isinstance(days_birth, float) or days_birth > 0:  # Exemple de validation
            return jsonify({'error': 'Le days_birth doit être un numérique négatif'}), 400

        # 4. Traitement des données
        # Mets les données dans un array 
        X = np.array([])
        for field in required_fields:
            X = np.append(X, data[field])
        # X = X.reshape(1,-1)  # Reshape pour 1 client
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
# [END cloudrun_helloworld_service]