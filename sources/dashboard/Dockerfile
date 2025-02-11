# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster  
# Utiliser une image de base Python plus légère et optimisée

WORKDIR /app  
# Définir le répertoire de travail dans le conteneur

COPY requirements.txt .  
# Copier seulement le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt  
# Installer les dépendances (cache désactivé pour une image plus petite)

COPY . .  
# Copier tout le code source (plus simple et efficace)

# Exposer le port sur lequel Streamlit s'exécute
EXPOSE 8501

# Démarrer l'application Streamlit
CMD ["streamlit", "run", "dashboard.py"]