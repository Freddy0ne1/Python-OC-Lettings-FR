from django.contrib import admin
from .models import Letting, Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Configuration de l'admin pour Address.
    """
    # Affichage des champs dans l'admin
    list_display = ('number', 'street', 'city', 'state', 'zip_code')
    # Champs de recherche
    search_fields = ('city', 'street', 'state')
    # Filtres
    list_filter = ('state', 'city')

@admin.register(Letting)
class LettingAdmin(admin.ModelAdmin):
    """
    Configuration de l'admin pour Letting.
    """
    # Affichage des champs dans l'admin
    list_display = ('title', 'address')
    # Champs de recherche
    search_fields = ('title',)
