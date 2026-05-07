# 🏠 OC Lettings

Application web de gestion de locations immobilières développée avec Django.

> Projet Module 13 - OpenClassrooms : Mise à l'échelle d'une application Django avec une architecture modulaire.

---

## 📋 Sommaire

- [Présentation](#-présentation)
- [Technologies utilisées](#-technologies-utilisées)
- [Installation locale](#-installation-locale)
- [Lancer le site](#-lancer-le-site)
- [Les tests](#-les-tests)
- [Linting (vérification du code)](#-linting)
- [Docker](#-docker)
- [Pipeline CI/CD](#-pipeline-cicd)
- [Déploiement](#-déploiement)
- [Monitoring (Sentry)](#-monitoring-sentry)
- [Documentation](#-documentation)
- [Architecture du projet](#-architecture-du-projet)
- [Contribuer](#-contribuer)

---

## 🎯 Présentation

OC Lettings est un site web qui permet de consulter des **locations immobilières** et des **profils utilisateurs**.

Le projet initial était une application **monolithique** (tout le code dans un seul dossier). Il a été refactorisé en une **architecture modulaire** avec :

- Une application `lettings` pour les locations
- Une application `profiles` pour les profils utilisateurs
- Un pipeline CI/CD qui teste, construit et déploie automatiquement à chaque modification

---

## 🛠 Technologies utilisées

| Technologie | Rôle | Pourquoi ? |
|-------------|------|------------|
| **Python 3.10** | Langage principal | Stable et compatible avec Django 3.0 |
| **Django 3.0** | Framework web | Framework Python le plus populaire pour le web |
| **SQLite** | Base de données | Simple, pas besoin de serveur de base de données |
| **Docker** | Conteneurisation | Environnement identique partout (dev, CI, prod) |
| **GitHub Actions** | Pipeline CI/CD | Automatise tests, build et déploiement |
| **Render** | Hébergement | Gratuit, supporte Docker nativement |
| **Sentry** | Monitoring erreurs | Capture les bugs automatiquement en production |
| **Sphinx** | Documentation | Génère une doc technique professionnelle |
| **WhiteNoise** | Fichiers statiques | Sert les CSS/JS sans serveur web supplémentaire |
| **Gunicorn** | Serveur production | Serveur WSGI performant (remplace `runserver`) |

---

## 💻 Installation locale

### Prérequis

- **Python 3.10** - [Télécharger ici](https://www.python.org/downloads/)
- **Git** - [Télécharger ici](https://git-scm.com/downloads)
- **Docker** (optionnel) - [Télécharger ici](https://www.docker.com/products/docker-desktop/)

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/Freddy0ne1/Python-OC-Lettings-FR.git
cd Python-OC-Lettings-FR
```

### Étape 2 : Créer un environnement virtuel

Un environnement virtuel isole les dépendances du projet pour ne pas interférer avec les autres projets Python sur ta machine.

```bash
# Créer l'environnement virtuel
python -m venv env

# L'activer
# Sur Linux / Mac :
source env/bin/activate

# Sur Windows :
env\Scripts\activate
```

> 💡 Tu sais que l'environnement est activé quand tu vois `(env)` au début de la ligne dans le terminal.

### Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

Cette commande installe toutes les librairies listées dans le fichier `requirements.txt` (Django, pytest, flake8, etc.).

### Étape 4 : Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet :

```bash
# Linux / Mac
touch .env

# Windows (PowerShell)
New-Item .env
```

Ajoute ce contenu dans le fichier `.env` :

```env
SECRET_KEY=une-cle-secrete-quelconque
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

> ⚠️ Le fichier `.env` ne doit **jamais** être poussé sur GitHub. Il est listé dans `.gitignore`.

### Étape 5 : Appliquer les migrations

Les migrations créent les tables dans la base de données.

```bash
python manage.py migrate
```

---

## 🚀 Lancer le site

```bash
python manage.py runserver
```

Ouvre ton navigateur et va sur : **http://localhost:8000**

### Pages disponibles

| URL | Description |
|-----|-------------|
| `/` | Page d'accueil |
| `/lettings/` | Liste des locations |
| `/lettings/1/` | Détail d'une location |
| `/profiles/` | Liste des profils |
| `/profiles/HeadlinesGaworworker/` | Détail d'un profil |
| `/admin/` | Interface d'administration |

### Accès admin

```
Identifiant : admin
Mot de passe : Abc1234!
```

---

## ✅ Les tests

Les tests vérifient automatiquement que le code fonctionne correctement.

### Lancer tous les tests

```bash
pytest
```

### Résultat attendu

```
36 tests passés, couverture : 91%
```

### Ce que les tests vérifient

- **Tests des modèles** : Les objets (Address, Letting, Profile) se créent correctement
- **Tests des vues** : Les pages retournent le bon statut HTTP (200, 404)
- **Tests des URLs** : Les routes fonctionnent correctement

### Voir le rapport de couverture en HTML

```bash
pytest --cov=. --cov-report=html
```

Puis ouvre `htmlcov/index.html` dans ton navigateur. Les lignes en vert sont testées, celles en rouge ne le sont pas.

---

## 🔍 Linting

Le linting vérifie que le code respecte les règles de style Python (PEP 8).

```bash
flake8
```

Si aucune erreur ne s'affiche, le code est propre ! ✅

### Configuration

Les règles de flake8 sont définies dans `setup.cfg` :

```ini
[flake8]
max-line-length = 99
exclude = */migrations/*, env, venv, .git, __pycache__
```

---

## 🐳 Docker

Docker permet de faire tourner l'application dans un conteneur isolé, identique partout.

### Télécharger l'image depuis Docker Hub

```bash
docker pull freddy0ne/oc-lettings:latest
```

### Lancer le site avec Docker

```bash
docker run -p 8000:8000 \
  -e SECRET_KEY="ma-cle-secrete" \
  -e DEBUG="False" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  freddy0ne/oc-lettings:latest
```

Puis ouvre **http://localhost:8000**

### Construire l'image localement

```bash
docker build -t oc-lettings:latest .
```

---

## ⚡ Pipeline CI/CD

À chaque `git push` sur la branche `master`, GitHub Actions exécute automatiquement :

```
git push origin master
        │
        ▼ (20 secondes)
┌─────────────────────┐
│  1. TESTS & LINTING │  flake8 + pytest (36 tests, couverture > 80%)
└─────────┬───────────┘
          │ Si tout passe ✅
          ▼ (24 secondes)
┌─────────────────────┐
│  2. BUILD DOCKER    │  Construit l'image et la pousse sur Docker Hub
└─────────┬───────────┘
          │ Si tout passe ✅
          ▼ (3 secondes)
┌─────────────────────┐
│  3. DÉPLOIEMENT     │  Déclenche le déploiement sur Render
└─────────────────────┘
```

**Temps total : ~55 secondes** entre le push et le site mis à jour en production.

### Où voir le pipeline

1. Aller sur [GitHub Actions](https://github.com/Freddy0ne1/Python-OC-Lettings-FR/actions)
2. Cliquer sur **CI/CD Pipeline OC Lettings**
3. Voir les 3 jobs (vert = réussi, rouge = échoué)

### Secrets GitHub nécessaires

Ces valeurs sont stockées dans **Settings > Secrets and variables > Actions** :

| Secret | Description |
|--------|-------------|
| `SECRET_KEY` | Clé secrète Django |
| `DOCKER_USERNAME` | Username Docker Hub |
| `DOCKER_PASSWORD` | Token d'accès Docker Hub |
| `RENDER_DEPLOY_HOOK` | URL de déploiement Render |
| `SENTRY_DSN` | URL de connexion Sentry |

---

## 🌍 Déploiement

Le site est déployé automatiquement sur **Render** à chaque push sur `master`.

### Variables d'environnement sur Render

| Variable | Valeur |
|----------|--------|
| `SECRET_KEY` | (clé secrète générée) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com,localhost` |
| `SENTRY_DSN` | (DSN du projet Sentry) |

---

## 🐛 Monitoring (Sentry)

**Sentry** capture automatiquement les erreurs en production.

### Comment ça fonctionne

1. Le SDK `sentry-sdk` est installé dans Django
2. Quand une erreur se produit, Sentry la capture automatiquement
3. Tu reçois une notification avec le détail de l'erreur

### Configuration

Sentry se configure uniquement via la variable d'environnement `SENTRY_DSN`. Si cette variable n'est pas définie (en local par exemple), Sentry ne se charge pas.

---

## 📖 Documentation

La documentation technique est générée avec **Sphinx** et hébergée sur **Read The Docs**.

📚 **Lire la documentation** : [oc-lettings-freddy0ne.readthedocs.io](https://oc-lettings-freddy0ne.readthedocs.io)

### Générer la documentation localement

```bash
cd docs
make html
```

Puis ouvre `docs/build/html/index.html` dans ton navigateur.

---

## 📂 Architecture du projet

```
Python-OC-Lettings-FR/
│
├── .github/workflows/         # Pipeline CI/CD
│   └── ci-cd.yml              # Configuration GitHub Actions
│
├── docs/                      # Documentation Sphinx
│   └── source/
│       ├── conf.py            # Configuration Sphinx
│       └── *.rst              # Pages de documentation
│
├── lettings/                  # App des locations
│   ├── models.py              # Modèles : Address, Letting
│   ├── views.py               # Vues : liste et détail des locations
│   ├── urls.py                # URLs : /lettings/, /lettings/<id>/
│   ├── admin.py               # Configuration admin Django
│   ├── tests.py               # Tests unitaires
│   └── templates/lettings/    # Templates HTML
│
├── profiles/                  # App des profils
│   ├── models.py              # Modèle : Profile
│   ├── views.py               # Vues : liste et détail des profils
│   ├── urls.py                # URLs : /profiles/, /profiles/<username>/
│   ├── admin.py               # Configuration admin Django
│   ├── tests.py               # Tests unitaires
│   └── templates/profiles/    # Templates HTML
│
├── oc_lettings_site/          # Configuration Django
│   ├── settings.py            # Paramètres du projet
│   ├── urls.py                # URLs principales
│   └── views.py               # Vue de la page d'accueil
│
├── templates/                 # Templates globaux
│   ├── index.html             # Page d'accueil
│   ├── 404.html               # Page erreur 404
│   └── 500.html               # Page erreur 500
│
├── static/                    # Fichiers CSS, JS, images
├── Dockerfile                 # Image Docker
├── .dockerignore              # Fichiers exclus de Docker
├── .readthedocs.yaml          # Configuration Read The Docs
├── requirements.txt           # Dépendances Python
├── setup.cfg                  # Configuration pytest et flake8
└── manage.py                  # Point d'entrée Django
```

---

## 🤝 Contribuer

1. **Fork** le projet
2. Crée une branche : `git checkout -b ma-feature`
3. Fais tes modifications
4. Lance les tests : `pytest`
5. Vérifie le linting : `flake8`
6. Commit : `git commit -m "feat: description"`
7. Push : `git push origin ma-feature`
8. Ouvre une **Pull Request**

---

## 📎 Liens utiles

| Ressource | Lien |
|-----------|------|
| Repository GitHub | [github.com/Freddy0ne1/Python-OC-Lettings-FR](https://github.com/Freddy0ne1/Python-OC-Lettings-FR) |
| Docker Hub | [hub.docker.com/r/freddy0ne/oc-lettings](https://hub.docker.com/r/freddy0ne/oc-lettings) |
| Documentation | [oc-lettings-freddy0ne.readthedocs.io](https://oc-lettings-freddy0ne.readthedocs.io) |

---

Développé par **Freddy0ne** dans le cadre du Module 13 OpenClassrooms.
