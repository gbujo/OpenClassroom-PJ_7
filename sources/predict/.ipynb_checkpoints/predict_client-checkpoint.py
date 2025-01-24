# Module prédiction client

def predict_client(id_client):
    # Mode bouchon
    decision = 'Client à risque'
    score = 70.0
    seuil_decision = 60.0
    return decision, score, seuil_decision