import logging
from django.shortcuts import render, get_object_or_404
from .models import Letting

# Création d'un logger pour cette vue
logger = logging.getLogger(__name__)

# Vue pour afficher la liste des locations
def index(request):
    """
    vue listant toutes les locations disponibles.

    Context:
        lettings_list: QuerySet des tous les objects Letting
    Template:
        lettings/index.html
    """
    # Affichage du message de log
    logger.info("Affichage de la liste des locations")
    # Récupération de la liste des locations
    lettings_list = Letting.objects.all()
    # Création du contexte
    context = {'lettings_list': lettings_list}
    # Rendu de la vue
    return render(request, 'lettings/index.html', context)

# Vue pour afficher une location spécifique
def letting(request, letting_id):
    """
    vue affichant le détail d'une location.

    Args:
        letting_id (int): Identifiant de la location.

    Context:
        title: Titre de la location
        address: Objet Address correspondant à l'ID fourni        
    Template:
        lettings/letting.html
    """
    # Affichage du message de log
    logger.info(f"Accès au détail de la location n° {letting_id}")
    # Récupération de la location
    letting = get_object_or_404(Letting, id=letting_id)
    # Création du contexte
    context = {
        'title': letting.title, 
        'address': letting.address
    }
    # Rendu de la vue
    return render(request, 'lettings/letting.html', context)