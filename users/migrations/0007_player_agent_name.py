# Generated by Django 5.0.1 on 2024-01-17 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_player_in_waiting'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='agent_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
