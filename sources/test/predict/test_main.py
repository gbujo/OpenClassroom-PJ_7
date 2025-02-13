import pytest
from sources.predict.main import main as app  # Importez votre application Flask

@pytest.fixture
def client():
    """Crée un client de test pour l'application Flask."""
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    """Teste la route '/'."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello OC-PJ7 World!" in response.data

def test_lire_txt_fichier_trouve(client):
    """Teste la route '/liretxt' lorsque le fichier existe."""
    # Créer un fichier test.txt pour ce test
    with open("test.txt", "w") as f:
        f.write("Ceci est un test.")

    response = client.get('/liretxt')
    assert response.status_code == 200
    assert b"Fichier test.txt : Ceci est un test." in response.data

    # Supprimer le fichier test.txt après le test
    import os
    os.remove("test.txt")

def test_lire_txt_fichier_non_trouve(client):
    """Teste la route '/liretxt' lorsque le fichier n'existe pas."""
    response = client.get('/liretxt')
    assert response.status_code == 404
    assert b"Le fichier n'a pas \xc3\xa9t\xc3\xa9 trouv\xc3\xa9." in response.data # Attention à l'encodage UTF-8

def test_predictbouchon(client):
    """Teste la route '/predictbouchon'."""
    response = client.get('/predictbouchon')
    assert response.status_code == 200
    assert response.is_json  # Vérifie que la réponse est au format JSON
    data = response.get_json()
    assert 'decision' in data
    assert 'score' in data
    assert 'seuil_decision' in data

def test_APIpredict_donnees_valides(client):
    """Teste la route '/api/predict' avec des données valides."""
    data = {
        'DAYS_BIRTH': -1000.0,
        'CODE_GENDER_F': 'F',
        'FLAG_RISKED_ORGANIZATION_TYPE': 0,
        'RATIO_INCOME_TO_FAM_MEMBERS': 1.5,
        'FLAG_STABLE_INCOME_TYPE': 1,
        'EXT_SOURCE_2': 0.5,
        'AMT_ALL_SUM_MEAN': 10000.0,
        'RATIO_ALL_SUM_DEBT_TO_INCOME': 0.2,
        'RATIO_ALL_SUM_OVERDUE_TO_INCOME': 0.01,
        'RATIO_ALL_MAX_OVERDUE_TO_INCOME': 0.05
    }
    response = client.post('/api/predict', json=data)
    assert response.status_code == 200
    assert response.is_json
    result = response.get_json()
    assert 'decision' in result
    assert 'score' in result
    assert 'seuil_decision' in result

def test_APIpredict_donnees_invalides(client):
    """Teste la route '/api/predict' avec des données invalides (champ manquant)."""
    data = {
        'DAYS_BIRTH': -1000.0,
        'CODE_GENDER_F': 'F',
        # 'FLAG_RISKED_ORGANIZATION_TYPE': 0,  # Champ manquant
        'RATIO_INCOME_TO_FAM_MEMBERS': 1.5,
        'FLAG_STABLE_INCOME_TYPE': 1,
        'EXT_SOURCE_2': 0.5,
        'AMT_ALL_SUM_MEAN': 10000.0,
        'RATIO_ALL_SUM_DEBT_TO_INCOME': 0.2,
        'RATIO_ALL_SUM_OVERDUE_TO_INCOME': 0.01,
        'RATIO_ALL_MAX_OVERDUE_TO_INCOME': 0.05
    }
    response = client.post('/api/predict', json=data)
    assert response.status_code == 400
    assert response.is_json
    error_data = response.get_json()
    assert 'error' in error_data
    assert "Le champ \"FLAG_RISKED_ORGANIZATION_TYPE\" est obligatoire" in error_data['error']

# Ajoutez d'autres tests pour couvrir tous les cas possibles (erreurs, valeurs limites, etc.)