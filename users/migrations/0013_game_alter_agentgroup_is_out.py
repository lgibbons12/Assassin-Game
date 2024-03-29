# Generated by Django 5.0.1 on 2024-02-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_agentgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='agentgroup',
            name='is_out',
            field=models.BooleanField(default=True),
        ),
    ]
