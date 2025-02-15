# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster  
# Utiliser une image de base Python plus légère et optimisée

WORKDIR /app  
# Définir le répertoire de travail dans le conteneur

# Upgrade pip par rapport à l'image FROM
#RUN pip install --upgrade pip

COPY requirements.txt .  
# Copier seulement le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt  
# Installer les dépendances (cache désactivé pour une image plus petite)

COPY . .  
RUN chmod 644 model.pkl
# Copier tout le code source (plus simple et efficace)
# COPY /sources/predict/model.pkl .

# Installation de mon package predict_package (défini dans pyproject.toml)
RUN pip install .

EXPOSE 8080  
# Exposer le port

# Utiliser Gunicorn pour servir l'application Flask en production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]  # Important pour Cloud Run