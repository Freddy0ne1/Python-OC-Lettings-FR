import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse, resolve


@pytest.mark.django_db
class TestIndexView:
    """Tests de la page d'accueil."""

    def test_index_returns_200(self, client):
        """Test que la page d'accueil retourne HTTP 200."""
        url = reverse('index')
        response = client.get(url)
        assert response.status_code == 200

    def test_index_uses_correct_template(self, client):
        """Test que la page d'accueil utilise le bon template."""
        url = reverse('index')
        response = client.get(url)
        assert 'index.html' in [t.name for t in response.templates]


class TestIndexURL:
    """Tests de l'URL de la page d'accueil."""

    def test_index_url(self):
        """Test que / pointe vers la bonne vue."""
        url = reverse('index')
        assert url == '/'

    def test_index_resolves(self):
        """Test que / se resout vers la vue index."""
        resolver = resolve('/')
        assert resolver.view_name == 'index'


@pytest.fixture
def superuser_env(monkeypatch):
    """Retire les variables du superutilisateur pour partir d'un etat connu."""
    for name in ('DJANGO_SUPERUSER_USERNAME', 'DJANGO_SUPERUSER_PASSWORD',
                 'DJANGO_SUPERUSER_EMAIL'):
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


@pytest.mark.django_db
class TestEnsureAdminCommand:
    """Tests de la commande ensure_admin (compte admin pilote par l'environnement)."""

    def test_sans_mot_de_passe_verrouille_le_compte_existant(self, superuser_env):
        """Sans DJANGO_SUPERUSER_PASSWORD, l'ancien mot de passe ne fonctionne plus."""
        User.objects.create_superuser('admin', 'admin@example.com', 'ancien-mot-de-passe')
        call_command('ensure_admin')
        admin = User.objects.get(username='admin')
        assert not admin.has_usable_password()
        assert not admin.check_password('ancien-mot-de-passe')

    def test_sans_mot_de_passe_ne_cree_aucun_compte(self, superuser_env):
        """Sans DJANGO_SUPERUSER_PASSWORD et sans compte, rien n'est cree."""
        call_command('ensure_admin')
        assert not User.objects.filter(username='admin').exists()

    def test_avec_mot_de_passe_cree_le_superutilisateur(self, superuser_env):
        """Avec DJANGO_SUPERUSER_PASSWORD, le superutilisateur est cree."""
        superuser_env.setenv('DJANGO_SUPERUSER_PASSWORD', 'nouveau-secret-42')
        superuser_env.setenv('DJANGO_SUPERUSER_EMAIL', 'moi@example.com')
        call_command('ensure_admin')
        admin = User.objects.get(username='admin')
        assert admin.is_superuser and admin.is_staff
        assert admin.email == 'moi@example.com'
        assert admin.check_password('nouveau-secret-42')

    def test_avec_mot_de_passe_remplace_l_ancien(self, superuser_env):
        """Avec DJANGO_SUPERUSER_PASSWORD, un compte existant prend le nouveau mot de passe."""
        User.objects.create_user('admin', password='ancien-mot-de-passe')
        superuser_env.setenv('DJANGO_SUPERUSER_PASSWORD', 'nouveau-secret-42')
        call_command('ensure_admin')
        admin = User.objects.get(username='admin')
        assert admin.is_superuser and admin.is_staff
        assert admin.check_password('nouveau-secret-42')
        assert not admin.check_password('ancien-mot-de-passe')

    def test_nom_du_compte_configurable(self, superuser_env):
        """DJANGO_SUPERUSER_USERNAME choisit le compte a gerer."""
        superuser_env.setenv('DJANGO_SUPERUSER_USERNAME', 'freddy')
        superuser_env.setenv('DJANGO_SUPERUSER_PASSWORD', 'nouveau-secret-42')
        call_command('ensure_admin')
        assert User.objects.get(username='freddy').check_password('nouveau-secret-42')
        assert not User.objects.filter(username='admin').exists()
