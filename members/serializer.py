from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Member,Cotisation
from django.contrib.auth.models import User

#serializer for member
class MemberSerializer(ModelSerializer):
    # Champs supplémentaires pour l'utilisateur
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Member
        fields = [
            "username",  # Champ lié au modèle User
            "password",  # Champ lié au modèle User
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