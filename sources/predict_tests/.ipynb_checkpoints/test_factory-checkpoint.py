from predict import create_app


def test_config():
    assert not create_app().testing


def test_hello(client):
    response = client.get('/hello')
    assert response.status_code == 404
#    assert response.data == b'Hello, World!'

def test_hello_world(client):
    """Teste la route '/'."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello OC-PJ7 World!" in response.data