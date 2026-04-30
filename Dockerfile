# Image de base Python 3.10 (stable, compatible avec Django 3.0)
FROM python:3.10-slim

# Variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
PYTHONDONTWRITEBYTECODE=1 \
PORT=8000

# Repertoire de travail dans le container
WORKDIR /app

# Installer les dependances systeme
RUN apt-get update && apt-get install -y \
gcc \
&& rm -rf /var/lib/apt/lists/*

# Copier requirements.txt en premier (optimisation cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Creer un utilisateur non-root pour la securite
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Exposer le port
EXPOSE $PORT

# Appliquer les migrations et demarrer gunicorn
CMD python manage.py migrate --noinput && gunicorn
oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT
