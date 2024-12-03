from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from .models import Evenement
from members.serializer import MemberSerializer

class EvenementSerializer(ModelSerializer):
    participants = SerializerMethodField()

    class Meta:
        model = Evenement
        fields = ["id_evenement", "titre", "description", "date", "lieu", "participants"]

    def get_participants(self, obj):
        request = self.context.get('request')  # Récupérer l'utilisateur depuis le contexte
        if request and request.user.is_staff:
            # Les administrateurs voient tous les détails des participants
            return MemberSerializer(obj.participants.all(), many=True).data
        # Les autres utilisateurs ne voient rien
        return None