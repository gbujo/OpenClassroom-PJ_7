import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello Guillaume {name}!"

@app.route("/test")
def test_url():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Test d'URL"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))  # si code appelé en local, le serveur Web écoute le prot spécifié dans la variable d'environnement PORT