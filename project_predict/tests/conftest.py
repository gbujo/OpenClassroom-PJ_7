# From https://flask.palletsprojects.com/en/stable/tutorial/tests/

import pytest
# Si j'importe create_app, mon client ne renvoit que des erreurs 404
#from predict import create_app  # Importe une fonction

# fonctionne si je prends directement l'app de predict.main
from predict.main import app

# Piste : en prenant directemetn app, l'object n'a pas d'attribu config !!!!

#@pytest.fixture()
#def app():
#    app = create_app()  # Pris directement depuis predict.main
#    app.config.update({
#        "TESTING": True
#    })
#
#    # other setup can go here
#
#    yield app
#
#    # clean up / reset resources at end of tests here


@pytest.fixture()
def client():
#def client(app):
    return app.test_client()


