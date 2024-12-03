from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Evenement
from members.models import Member
from .serializer import EvenementSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
import csv
from django.http import HttpResponse


# Create your views here.
class CreateEventApiView(CreateAPIView):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [IsAdminUser]

class ListEventApiView(ListAPIView):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    def get_serializer_context(self):
        return {'request': self.request}

class RetrieveEvenetApiByIdView(RetrieveAPIView):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    lookup_field = "id_evenement"
    def get_serializer_context(self):
        return {'request': self.request}

class UpdateEventApiView(UpdateAPIView):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [IsAdminUser]

class DeleteEventApiView(DestroyAPIView):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [IsAdminUser]

#classe pour gérer l'inscription d'un membre a un event
class InscriptionEvenementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        membre_id = request.data.get("id_membre") 
        evenement_id = request.data.get("id_evenement")  

        # Récupérer le membre et l'événement
        try:
            membre = Member.objects.get(id_membre=membre_id)
            evenement = Evenement.objects.get(id_evenement=evenement_id)

        except Member.DoesNotExist:
            return Response({"error": "Membre non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si le membre a réglé sa cotisation
        if not membre.statut_adhesion:
            return Response({"error": "Votre cotisation n'est pas réglée."}, status=status.HTTP_403_FORBIDDEN)

        # Ajouter le membre comme participant s'il n'est pas déjà inscrit
        if membre in evenement.participants.all():
            return Response({"error": "Vous êtes déjà inscrit à cet événement."}, status=status.HTTP_400_BAD_REQUEST)

        evenement.participants.add(membre)
        return Response({"message": "Inscription réussie."}, status=status.HTTP_200_OK)

class AnnulationInscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        membre_id = request.data.get("id_membre")
        evenement_id = request.data.get("id_evenement")

        try:
            membre = Member.objects.get(id_membre=membre_id)
            evenement = Evenement.objects.get(id_evenement=evenement_id)
        except Member.DoesNotExist:
            return Response({"error": "Membre non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        if membre not in evenement.participants.all():
            return Response({"error": "Vous n'êtes pas inscrit à cet événement."}, status=status.HTTP_400_BAD_REQUEST)

        evenement.participants.remove(membre)
        return Response({"message": "Inscription annulée avec succès."}, status=status.HTTP_200_OK)
    



class ExportParticipantsView(APIView):
    """
    Permettre d’exporter les listes des événements ou des participants au format CSV pour analyse.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, id_evenement):
        try:
            evenement = Evenement.objects.get(id_evenement=id_evenement)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Préparer le fichier CSV
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="participants_{evenement.titre}.csv"'

        writer = csv.writer(response)
        writer.writerow(["Nom complet", "Email", "Département", "Année d'étude"])

        for participant in evenement.participants.all():
            writer.writerow([participant.full_name, participant.email, participant.departement, participant.annee_etude])

        return response

