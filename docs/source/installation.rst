Installation
============

Prerequis
---------

* Python 3.10
* Git
* Docker (optionnel)

Installation locale
-------------------

1. Cloner le repository ::

    git clone https://github.com/Freddy0ne1/Python-OC-Lettings-FR.git
    cd Python-OC-Lettings-FR

2. Creer l'environnement virtuel ::

    python -m venv venv
    source venv/bin/activate

3. Installer les dependances ::

    pip install -r requirements.txt

4. Appliquer les migrations ::

    python manage.py migrate

5. Lancer le serveur ::

    python manage.py runserver

Le site est accessible sur http://localhost:8000

Identifiants admin : admin / Abc1234!