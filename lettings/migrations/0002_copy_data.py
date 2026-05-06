from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    """Copie les donnees de oc_lettings_site vers lettings."""
    # Récupération des anciens modèles
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    # Récupération des anciens modèles
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    # Récupération des nouveaux modèles
    NewAddress = apps.get_model('lettings', 'Address')
    # Récupération des nouveaux modèles
    NewLetting = apps.get_model('lettings', 'Letting')
    # Copie des données
    for old_addr in OldAddress.objects.all():
        NewAddress.objects.create(
            id=old_addr.id,
            number=old_addr.number,
            street=old_addr.street,
            city=old_addr.city,
            state=old_addr.state,
            zip_code=old_addr.zip_code,
            country_iso_code=old_addr.country_iso_code
        )
    for old_let in OldLetting.objects.all():
        NewLetting.objects.create(
            id=old_let.id,
            title=old_let.title,
            address_id=old_let.address_id
        )



def reverse_copy(apps, schema_editor):
    """Rollback : vider les nouvelles tables."""
    # Suppression des données
    apps.get_model('lettings', 'Letting').objects.all().delete()
    # Suppression des données
    apps.get_model('lettings', 'Address').objects.all().delete()


class Migration(migrations.Migration):
    # Dépendances
    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]
    # Opérations
    operations = [
        migrations.RunPython(copy_lettings_data, reverse_copy),
    ]