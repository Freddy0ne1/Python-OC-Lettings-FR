Deploiement
===========

Pipeline CI/CD
--------------

A chaque push sur master, GitHub Actions execute :

1. **Tests** : flake8 + pytest (coverage > 80%)
2. **Build Docker** : image poussee sur Docker Hub
3. **Deploy** : site deploye sur Render

Configuration requise
---------------------

Secrets GitHub Actions :

* ``SECRET_KEY`` : Cle secrete Django
* ``DOCKER_USERNAME`` : Username Docker Hub
* ``DOCKER_PASSWORD`` : Token Docker Hub
* ``RENDER_DEPLOY_HOOK`` : URL webhook Render
* ``SENTRY_DSN`` : DSN Sentry

Variables d'environnement sur Render :

* ``SECRET_KEY`` : Cle secrete Django (obligatoire quand ``DEBUG`` vaut ``False``)
* ``DJANGO_SUPERUSER_PASSWORD`` : mot de passe du compte admin ; sans elle, le compte est verrouille
* ``DJANGO_SUPERUSER_USERNAME`` : nom du compte admin (``admin`` par defaut)

Recuperer l'image Docker
-------------------------

::

    docker pull freddy0ne/oc-lettings:latest
    docker run -p 8000:8000 freddy0ne/oc-lettings:latest