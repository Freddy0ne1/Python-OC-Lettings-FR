from django.db import migrations


class Migration(migrations.Migration):
    """
    Supprime les anciens modèles de oc_lettings_site.
    S'exécute seulement après que les données ont été copiées vers les nouveaux modèles.
    """
    # Dépendances
    dependencies = [
        ('oc_lettings_site', '0001_initial'),
        ('lettings', '0002_copy_data'),
        ('profiles', '0002_copy_data'),
    ]

    # Opérations
    operations = [
        migrations.DeleteModel(name='Profile'),
        migrations.DeleteModel(name='Letting'),
        migrations.DeleteModel(name='Address'),
    ]
