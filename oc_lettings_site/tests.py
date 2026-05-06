import pytest
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
