from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member, Cotisation
from datetime import date

@receiver(post_save, sender=Member)
def create_cotisation(sender, instance, created, **kwargs):
    """
    Crée automatiquement une cotisation pour chaque nouveau membre.
    """
    if created:  # Vérifie si un membre a été créé
        # Calculer l'année académique en cours
        today = date.today()
        if today.month >= 9:  # De septembre à décembre
            annee_academique = f"{today.year}-{today.year + 1}"
        else:  # De janvier à août
            annee_academique = f"{today.year - 1}-{today.year}"

        # Créer une cotisation
        Cotisation.objects.create(
            membre=instance,
            montant=0.00,  # Montant par défaut
            statut=False,  # Non payé par défaut
            annee_academique=annee_academique
        )
