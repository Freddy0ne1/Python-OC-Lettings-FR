from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Modèle représentant le profil d'un utilisateur.

    Attributes:
        user (User): Utilisateur associé au profil (relation OneToOne)
        favorite_city (str): Ville favorite de l'utilisateur (optionnel)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """ Retourne le nom d'utilisateur sous forme de chaîne de caractères """
        return self.user.username # Affiche le nom d'utilisateur
