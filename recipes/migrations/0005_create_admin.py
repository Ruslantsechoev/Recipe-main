from django.db import migrations
from django.contrib.auth.models import User

def create_admin(apps, schema_editor):
    User.objects.create_superuser(
        username='Leej2',
        email='admin@example.com',
        password='9250'
    )

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]