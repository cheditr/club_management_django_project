from django.db import models
import uuid
from members.models import Member

# Create your models here.
class Evenement(models.Model):
    id_evenement=models.UUIDField(primary_key=True,default=uuid.uuid4)
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    lieu = models.CharField(max_length=100)
    participants = models.ManyToManyField(Member)