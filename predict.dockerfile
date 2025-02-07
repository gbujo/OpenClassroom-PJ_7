# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster  
# Utiliser une image de base Python plus légère et optimisée

WORKDIR /app  
# Définir le répertoire de travail dans le conteneur

COPY /sources/predict/requierements.txt .  
# Copier seulement le fichier requirements.txt
RUN pip install --no-cache-dir -r requierements.txt  
# Installer les dépendances (cache désactivé pour une image plus petite)

COPY /sources/predict/. .  
# Copier tout le code source (plus simple et efficace)
COPY /sources/predict/model.pkl .

EXPOSE 8080  
# Exposer le port

# Utiliser Gunicorn pour servir l'application Flask en production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]  # Important pour Cloud Run