import logging
from django.shortcuts import render, get_object_or_404
from .models import Profile

# Création d'un logger pour cette vue
logger = logging.getLogger(__name__)

# Vue pour afficher la liste des profils
def index(request):
    """
    Vue listant tous les profils utilisateurs.

    Context:
        profiles_list: QuerySet des tous les objects Profile
    Template:
        profiles/index.html
    """
    # Affichage du message de log
    logger.info("Affichage de la liste des profils")
    # Récupération de la liste des profils
    profiles_list = Profile.objects.all()
    # Création du contexte
    context = {'profiles_list': profiles_list}
    # Rendu de la vue
    return render(request, 'profiles/index.html', context)

# Vue pour afficher un profil spécifique
def profile(request, username):
    """
    Vue affichant le détail d'un profil utilisateur.

    Args:
        username (str): Nom d'utilisateur.

    Context:
        profile: Objet Profile correspondant au nom d'utilisateur fourni       
    Template:
        profiles/profile.html
    """
    # Affichage du message de log
    logger.info(f"Accès au détail du profil n° {username}")
    # Récupération du profil
    profile = get_object_or_404(Profile, user__username=username)
    # Création du contexte
    context = {'profile': profile}
    # Rendu de la vue
    return render(request, 'profiles/profile.html', context)