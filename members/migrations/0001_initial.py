# Generated by Django 5.1.3 on 2024-11-24 13:49

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id_membre', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('departement', models.CharField(max_length=100)),
                ('annee_etude', models.IntegerField()),
                ('statut_adhesion', models.BooleanField(default=False)),
                ('date_inscription', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cotisation',
            fields=[
                ('id_cotisation', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=6)),
                ('statut', models.BooleanField(default=False)),
                ('annee_academique', models.CharField(max_length=9)),
                ('membre', models.ForeignKey(db_column='id_membre', on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
    ]
