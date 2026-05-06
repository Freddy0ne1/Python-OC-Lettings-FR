from django.shortcuts import render


def index(request):
    """ Vue de la page d'accueil """
    return render(request, 'index.html')
