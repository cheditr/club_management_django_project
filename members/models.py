from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    id_membre = models.UUIDField(primary_key=True,default=uuid.uuid4)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    departement = models.CharField(max_length=100)
    annee_etude = models.IntegerField() # 1 ou 2 ou 3
    statut_adhesion = models.BooleanField(default=False)  
    date_inscription = models.DateField(auto_now_add=True)

class Cotisation(models.Model):
    id_cotisation = models.UUIDField(primary_key=True,default=uuid.uuid4)
    membre = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='id_membre')
    montant = models.DecimalField(max_digits=6, decimal_places=2)
    statut = models.BooleanField(default=False)  # Payé ou en attente
    annee_academique = models.CharField(max_length=9)
