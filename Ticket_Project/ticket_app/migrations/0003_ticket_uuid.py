# Generated by Django 4.2.5 on 2023-10-05 21:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_app', '0002_alter_location_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
