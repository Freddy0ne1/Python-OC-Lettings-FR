import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse, resolve

from profiles.models import Profile


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def user():
    """Cree un utilisateur de test."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        password='testpass123'
    )


@pytest.fixture
def sample_profile(user):
    """Cree un profil de test."""
    return Profile.objects.create(
        user=user,
        favorite_city='Paris'
    )


# ============================================================
# TESTS DES MODELES
# ============================================================

@pytest.mark.django_db
class TestProfileModel:
    """Tests unitaires du modele Profile."""
    
    def test_profile_str(self, sample_profile):
        """Test que __str__ retourne le nom d'utilisateur."""
        assert str(sample_profile) == 'testuser'
    
    def test_profile_creation(self, sample_profile, user):
        """Test la creation d'un profil."""
        assert sample_profile.user == user
        assert sample_profile.favorite_city == 'Paris'
    
    def test_profile_blank_city(self, user):
        """Test qu'on peut creer un profil sans ville favorite."""
        profile = Profile.objects.create(user=user, favorite_city='')
        assert profile.favorite_city == ''

    def test_profile_cascade_delete(self, sample_profile, user):
        """Test que la suppression du user supprime aussi le profil."""
        profile_id = sample_profile.id
        user.delete()
        assert not Profile.objects.filter(id=profile_id).exists()


# ============================================================
# TESTS DES VUES
# ============================================================

@pytest.mark.django_db
class TestProfilesViews:
    """Tests d'integration des vues profiles."""
    
    def test_index_returns_200(self, client, sample_profile):
        """Test que la liste des profils retourne HTTP 200."""
        url = reverse('profiles:index')
        response = client.get(url)
        assert response.status_code == 200
    
    def test_index_uses_correct_template(self, client, sample_profile):
        """Test que la vue index utilise le bon template."""
        url = reverse('profiles:index')
        response = client.get(url)
        assert 'profiles/index.html' in [t.name for t in response.templates]
    
    def test_index_contains_profile(self, client, sample_profile):
        """Test que la liste contient bien le profil cree."""
        url = reverse('profiles:index')
        response = client.get(url)
        assert sample_profile in response.context['profiles_list']

    def test_profile_detail_returns_200(self, client, sample_profile):
        """Test que la page detail retourne HTTP 200."""
        url = reverse('profiles:profile', kwargs={'username': 'testuser'})
        response = client.get(url)
        assert response.status_code == 200
        
    def test_profile_detail_uses_correct_template(self, client, sample_profile):
        """Test que la vue detail utilise le bon template."""
        url = reverse('profiles:profile', kwargs={'username': 'testuser'})
        response = client.get(url)
        assert 'profiles/profile.html' in [t.name for t in response.templates]
        
    def test_profile_detail_context(self, client, sample_profile):
        """Test que le contexte contient le bon profil."""
        url = reverse('profiles:profile', kwargs={'username': 'testuser'})
        response = client.get(url)
        assert response.context['profile'] == sample_profile
        
    def test_profile_detail_404(self, client):
        """Test qu'un username inexistant retourne HTTP 404."""
        url = reverse('profiles:profile', kwargs={'username': 'nonexistent'})
        response = client.get(url)
        assert response.status_code == 404


# ============================================================
# TESTS DES URLS
# ============================================================

class TestProfilesURLs:
    """Tests des URLs profiles."""
    def test_profiles_index_url(self):
        """Test que /profiles/ pointe vers la bonne vue."""
        url = reverse('profiles:index')
        assert url == '/profiles/'
    
    def test_profiles_index_resolves(self):
        """Test que /profiles/ se resout vers la vue index."""
        resolver = resolve('/profiles/')
        assert resolver.view_name == 'profiles:index'
    
    def test_profile_detail_url(self):
        """Test que /profiles/testuser/ pointe vers la bonne vue."""
        url = reverse('profiles:profile', kwargs={'username': 'testuser'})
        assert url == '/profiles/testuser/'
    
    def test_profile_detail_resolves(self):
        """Test que /profiles/testuser/ se resout vers la vue profile."""
        resolver = resolve('/profiles/testuser/')
        assert resolver.view_name == 'profiles:profile'
        assert resolver.kwargs == {'username': 'testuser'}
