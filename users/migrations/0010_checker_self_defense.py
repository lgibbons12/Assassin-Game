# Generated by Django 5.0.1 on 2024-01-25 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_player_have_eliminated_today"),
    ]

    operations = [
        migrations.AddField(
            model_name="checker",
            name="self_defense",
            field=models.BooleanField(default=False),
        ),
    ]
