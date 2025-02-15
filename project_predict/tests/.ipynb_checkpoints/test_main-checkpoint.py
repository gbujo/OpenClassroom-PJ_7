import pytest
#from predict import main

#@pytest.fixture
#def client():
#    """Crée un client de test pour l'application Flask."""
#    with app.test_client() as client:
#        yield client

# ici l'object client en paramètre des fonctions provient de la fixture dans conftest.py (retourne une app)

def test_hello_world(client):  
    """Teste la route '/'."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello OC-PJ7 World!" in response.data

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
        'CODE_GENDER_F': 1,
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

def test_APIpredict_aucune_donnee(client):
    """Teste la route '/api/predict' avec des données invalides (champ manquant)."""
    data = {}
    response = client.post('/api/predict', json=data)
    assert response.status_code == 400
    assert response.is_json
    error_data = response.get_json()
    assert 'error' in error_data
    assert 'Aucune donnée fournie' in error_data['error']

def test_APIpredict_donnee_manquante(client):
    """Teste la route '/api/predict' avec des données invalides (champ manquant)."""
    data = {
        'DAYS_BIRTH': -1000.0,
        'CODE_GENDER_F': 1,
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

def test_APIpredict_donnee_invalide1(client):
    """Teste la route '/api/predict' avec des données invalides (champ manquant)."""
    data = {
        'DAYS_BIRTH': +1000.0,  # Invalide
        'CODE_GENDER_F': 1,
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
    assert response.status_code == 400
    assert response.is_json
    error_data = response.get_json()
    assert 'error' in error_data
    assert 'Uniquement valeurs < 0 autorisées pour DAYS_BIRTH' in error_data['error']

def test_APIpredict_donnee_invalide2(client):
    """Teste la route '/api/predict' avec des données invalides (champ manquant)."""
    data = {
        'DAYS_BIRTH': -1000.0,
        'CODE_GENDER_F': 'F',  # Invalide
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
    assert response.status_code == 400
    assert response.is_json
    error_data = response.get_json()
    assert 'error' in error_data
#    assert 'Uniquement valeurs 0, 1 autorisées pour CODE_GENDER' in error_data['error']
    assert 'Erreur de type ou de format pour un des champs' in error_data['error']

