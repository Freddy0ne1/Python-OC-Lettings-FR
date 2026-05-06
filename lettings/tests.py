import pytest
from django.test import Client
from django.urls import reverse, resolve

from lettings.models import Letting, Address


# ============================================================
# FIXTURES : Donnees de test reutilisables
# ============================================================

@pytest.fixture
def address():
    """Crée une instance d'adresse de test"""
    return Address.objects.create(
        number=123,
        street='Main Street',
        city='Springfield',
        state='IL',
        zip_code='62701',
        country_iso_code='USA'
    )


@pytest.fixture
def sample_letting(address):
    """Crée une instance de letting de test avec une adresse associée"""
    return Letting.objects.create(
        title='Beautiful Apartment',
        address=address
    )


# ============================================================
# TESTS DES MODELES
# ============================================================
@pytest.mark.django_db
class TestAddressModel:
    """Tests unitaires du modele Address."""
    def test_address_str(self, address):
        """Test que __str__ retourne 'number street'."""
        assert str(address) == '123 Main Street'

    def test_address_creation(self, address):
        """Test la creation d'une adresse avec tous les champs."""
        assert address.number == 123
        assert address.street == 'Main Street'
        assert address.city == 'Springfield'
        assert address.state == 'IL'
        assert int(address.zip_code) == 62701
        assert address.country_iso_code == 'USA'

    def test_address_verbose_name_plural(self):
        """Test que le pluriel est 'Addresses' et non 'Addresss'."""
        assert Address._meta.verbose_name_plural == 'Addresses'
    

@pytest.mark.django_db
class TestLettingModel:
    """Tests unitaires du modele Letting."""
    def test_letting_str(self, sample_letting):
        """Test que __str__ retourne le titre."""
        assert str(sample_letting) == 'Beautiful Apartment'

    def test_letting_creation(self, sample_letting, address):
        """Test la creation d'une location."""
        assert sample_letting.title == 'Beautiful Apartment'
        assert sample_letting.address == address

    def test_letting_cascade_delete(self, sample_letting, address):
        """Test que supprimer l'adresse supprime la location."""
        letting_id = sample_letting.id
        address.delete()
        assert not Letting.objects.filter(id=letting_id).exists()

        
# ============================================================
# TESTS DES VUES
# ============================================================

@pytest.mark.django_db
class TestLettingsViews:
    """Tests d'integration des vues lettings."""
    def test_index_returns_200(self, client, sample_letting):
        """Test que la liste des lettings retourne HTTP 200."""
        url = reverse('lettings:index')
        response = client.get(url)
        assert response.status_code == 200

    def test_index_uses_correct_template(self, client, sample_letting):
        """Test que la vue index utilise le bon template."""
        url = reverse('lettings:index')
        response = client.get(url)
        assert 'lettings/index.html' in [t.name for t in response.templates]
        
    def test_index_contains_letting(self, client, sample_letting):
        """Test que la liste contient bien la location creee."""
        url = reverse('lettings:index')
        response = client.get(url)
        assert sample_letting in response.context['lettings_list']
        
    def test_letting_detail_returns_200(self, client, sample_letting):
        """Test que la page detail retourne HTTP 200."""
        url = reverse('lettings:letting', kwargs={'letting_id': sample_letting.id})
        response = client.get(url)
        assert response.status_code == 200

    def test_letting_detail_uses_correct_template(self, client, sample_letting):
        """Test que la vue detail utilise le bon template."""
        url = reverse('lettings:letting', kwargs={'letting_id':sample_letting.id})
        response = client.get(url)
        assert 'lettings/letting.html' in [t.name for t in response.templates]
        
    def test_letting_detail_context(self, client, sample_letting, address):
        """Test que le contexte contient le titre et l'adresse."""
        url = reverse('lettings:letting', kwargs={'letting_id':sample_letting.id})
        response = client.get(url)
        assert response.context['title'] == 'Beautiful Apartment'
        assert response.context['address'] == address

    def test_letting_detail_404(self, client):
        """Test qu'un ID inexistant retourne HTTP 404."""
        url = reverse('lettings:letting', kwargs={'letting_id': 9999})
        response = client.get(url)
        assert response.status_code == 404

# ============================================================
# TESTS DES URLS
# ============================================================
class TestLettingsURLs:
    """Tests des URLs lettings."""
    def test_lettings_index_url(self):
        """Test que /lettings/ pointe vers la bonne vue."""
        url = reverse('lettings:index')
        assert url == '/lettings/'
        
    def test_lettings_index_resolves(self):
        """Test que /lettings/ se resout vers la vue index."""
        resolver = resolve('/lettings/')
        assert resolver.view_name == 'lettings:index'
    
    def test_letting_detail_url(self):
        """Test que /lettings/1/ pointe vers la bonne vue."""
        url = reverse('lettings:letting', kwargs={'letting_id': 1})
        assert url == '/lettings/1/'
        
    def test_letting_detail_resolves(self):
        """Test que /lettings/1/ se resout vers la vue letting."""
        resolver = resolve('/lettings/1/')
        assert resolver.view_name == 'lettings:letting'
        assert resolver.kwargs == {'letting_id': 1}