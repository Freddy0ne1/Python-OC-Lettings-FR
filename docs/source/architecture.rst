Architecture
============

Structure du projet
-------------------

.. code-block:: text

    Python-OC-Lettings-FR/
    ├── oc_lettings_site/    <- Configuration Django
    │   ├── settings.py
    │   ├── urls.py
    │   └── views.py
    ├── lettings/            <- App locations
    │   ├── models.py (Address, Letting)
    │   ├── views.py
    │   └── urls.py
    ├── profiles/            <- App profils
    │   ├── models.py (Profile)
    │   ├── views.py
    │   └── urls.py
    ├── templates/
    └── static/

Modeles de donnees
------------------

**Address** : number, street, city, state, zip_code, country_iso_code

**Letting** : title, address (OneToOne vers Address)

**Profile** : user (OneToOne vers User), favorite_city

URLs
----

.. code-block:: text

    /                        -> Accueil
    /lettings/               -> Liste des locations
    /lettings/<id>/          -> Detail location
    /profiles/               -> Liste des profils
    /profiles/<username>/    -> Detail profil
    /admin/                  -> Administration