# Je teste avec la creat_app pour voir
import pytest
#from predict import create_app
#from predict.main import app
from flask import Flask 




#@pytest.fixture
#def client():
#    app = create_app()
#    app = Flask(__name__)
#    with app.test_client() as client:
#        yield client

#@pytest.fixture()
#def app():
#    app = create_app()
#    app.config.update({
#        "TESTING": True,
#        "DEBUG": True
#    })
#
#    # other setup can go here
#
#    yield app
#
#    # clean up / reset resources at end of tests here

#@pytest.fixture
#def client(app):
#    with app.test_client() as client:
#        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Hello" in rv.data


#def test_create_app1(app):
#    assert isinstance(app, Flask)
#    assert app.test_client() is None
#    assert app.name == 'predict'
#    assert app.config['DEBUG'] is True

def test_client_instance(client):
    # Vérifie que le client est une instance de Flask test client
    assert hasattr(client, 'get')
    assert hasattr(client, 'post')