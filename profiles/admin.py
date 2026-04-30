from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Configuration de l'admin pour Profile.
    """
    # Affichage des champs dans l'admin
    list_display = ('user', 'favorite_city')
    # Champs de recherche
    search_fields = ('user__username', 'favorite_city')
    # Filtres
    list_filter = ('favorite_city',)
    