from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Member,Cotisation
from django.contrib.auth.models import User

#serializer for member
class MemberSerializer(ModelSerializer):
    # Champs supplémentaires pour l'utilisateur lors de la création
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Member
        fields = [
            "username",  # Champ lié au modèle User (optionnel pour la mise à jour)
            "password",  # Champ lié au modèle User (optionnel pour la mise à jour)
            "full_name",
            "email",
            "departement",
            "annee_etude",
        ]

    def create(self, validated_data):
        # Extraire les données liées à User
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        email = validated_data["email"]  # L'email est partagé entre User et Member

        # Créer l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)

        # Créer le membre et le lier à l'utilisateur
        member = Member.objects.create(user=user, **validated_data)
        return member

    def update(self, instance, validated_data):
        # Mise à jour des champs du modèle Member uniquement
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.email = validated_data.get("email", instance.email)
        instance.departement = validated_data.get("departement", instance.departement)
        instance.annee_etude = validated_data.get("annee_etude", instance.annee_etude)
        instance.save()
        return instance

#serializer pour l'utiliser dans la table cotisation
class MemberMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id_membre", "full_name", "email"]  # Champs uniquement en lecture

class CotisationSerializer(ModelSerializer):
    membre = MemberMinimalSerializer(read_only=True)
    class Meta:
        model = Cotisation
        fields = ["id_cotisation","membre","montant","statut","annee_academique"]