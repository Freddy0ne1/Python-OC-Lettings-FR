from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class Address(models.Model):
    """
    Modèle représentant une adresse physique.

    Attributes :
        number (int): Numéro de rue (max 9999)
        street (str): Nom de la rue (max 64 caractères)
        city (str): Ville (max 64 caractères)
        state (str): État (2 caractères - code US)
        zip_code (int): Code postal (max 99999)
        country_iso_code (str): Code pays ISO (3 caractères)
    """
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        verbose_name_plural = "Addresses" # Corrige "Adresss" dans l'admin

    def __str__(self):
        """ Retourne l'adresse sous forme de chaîne de caractères """
        return f'{self.number} {self.street}' # Affiche l'adresse


class Letting(models.Model):
    """
    Modèle représentant une location immobilière.

    Attributes:
        title (str): Titre de l'annonce (max 256 caractères)
        address (Address): Adresse de la propriété (relation OneToOne)
    """
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """ Retourne le titre de la location sous forme de chaîne de caractères """
        return self.title # Affiche le titre de la location
