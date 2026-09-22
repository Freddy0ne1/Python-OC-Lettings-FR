import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Aligne le compte administrateur sur les variables d'environnement.

    Aucun mot de passe n'est ecrit dans le code ni dans l'image Docker :
    - avec DJANGO_SUPERUSER_PASSWORD, le compte est cree ou recoit ce mot de passe ;
    - sans cette variable, un compte existant est verrouille (aucune connexion possible).
    """

    help = "Cree, met a jour ou verrouille le superutilisateur selon l'environnement."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')

        if not password:
            user = User.objects.filter(username=username).first()
            if user is None:
                self.stdout.write("Aucun superutilisateur configure.")
                return
            user.set_unusable_password()
            user.save(update_fields=['password'])
            self.stdout.write(
                f"Compte '{username}' verrouille : DJANGO_SUPERUSER_PASSWORD absent."
            )
            return

        user, created = User.objects.get_or_create(username=username)
        user.is_staff = True
        user.is_superuser = True
        if email:
            user.email = email
        user.set_password(password)
        user.save()
        action = 'cree' if created else 'mis a jour'
        self.stdout.write(f"Superutilisateur '{username}' {action}.")
