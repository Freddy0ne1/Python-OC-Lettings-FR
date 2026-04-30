from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    """Copie les profils de oc_lettings_site vers profiles."""
    # Récupération des anciens modèles
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    # Récupération des nouveaux modèles
    NewProfile = apps.get_model('profiles', 'Profile')
    # Copie des données
    for old_prof in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old_prof.id,
            user_id=old_prof.user_id,
            favorite_city=old_prof.favorite_city
        )


def reverse_copy(apps, schema_editor):
    """Rollback : vider les nouveaux profils."""
    # Suppression des données
    apps.get_model('profiles', 'Profile').objects.all().delete()


class Migration(migrations.Migration):
    # Dépendances
    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]
    # Opérations
    operations = [
        migrations.RunPython(copy_profiles_data, reverse_copy),
    ]