from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from .models import Member,Cotisation
from .serializer import MemberSerializer,CotisationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Create your views here.
class SignUpView(APIView):
    permission_classes = [AllowAny]  # Accessible à tous

    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        
        # Valider les données
        if serializer.is_valid():
            serializer.save()  # Appelle la méthode `create` du sérialiseur
            return Response({"message": "Utilisateur et membre créés avec succès."}, status=status.HTTP_201_CREATED)
        
        # Retourner les erreurs de validation
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SignInView(APIView):
    """
    Vue pour permettre à un utilisateur de se connecter.
    """
    permission_classes = [AllowAny]  # Accessible à tous

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Vérifier que les champs sont fournis
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class ListMemberApiView(ListAPIView):
    queryset = Member.objects.select_related()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]  # Accessible uniquement aux utilisateurs authentifiés

    def get_queryset(self):
        # Si l'utilisateur est un administrateur, on retourne tous les membres
        if self.request.user.is_staff:
            return Member.objects.all()  # Admin peut voir tous les membres
        
        # Sinon, on retourne uniquement le membre associé à l'utilisateur connecté
        return Member.objects.filter(user=self.request.user)

class RetrieveMemberByIdApiView(RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = "id_membre"
    permission_classes = [IsAdminUser]



class DeleteMemberApiView(DestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]

class UpdateMemberApiView(UpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer 
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        # Si l'utilisateur est un administrateur, on retourne tous les membres
        if self.request.user.is_staff:
            return Member.objects.all()  # Admin peut voir tous les membres
        
        # Sinon, on retourne uniquement le membre associé à l'utilisateur connecté
        return Member.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()  # Assurer que l'objet retourné est celui du membre connecté  



#CRUD pour la classe Cotisation
class CreateCotisationApiView(CreateAPIView):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    permission_classes = [IsAdminUser]

class UpdateCotisationApiView(UpdateAPIView):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    permission_classes = [IsAdminUser]

class ListCotisationApiView(ListAPIView):
    serializer_class = CotisationSerializer
    permission_classes = [IsAuthenticated]  # Accessible uniquement aux utilisateurs authentifiés

    def get_queryset(self):
        user = self.request.user

        # Si l'utilisateur est un administrateur, il peut voir toutes les cotisations
        if user.is_superuser:
            return Cotisation.objects.all()

        # Sinon, retourner uniquement les cotisations associées au membre connecté
        return Cotisation.objects.filter(membre__user=user)

class RetrieveCotisationByIdApiView(RetrieveAPIView):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    lookup_field = "id_cotisation"
    permission_classes = [IsAdminUser]


class DeleteCotisationApiView(DestroyAPIView):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    permission_classes = [IsAdminUser]

