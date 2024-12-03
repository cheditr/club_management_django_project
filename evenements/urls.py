from django.urls import path,include
from .views import *


urlpatterns = [
    path('',ListEventApiView.as_view()),
    path('create/', CreateEventApiView.as_view()),
    path('<str:id_evenement>',RetrieveEvenetApiByIdView.as_view()),
    path('update/<str:pk>',UpdateEventApiView.as_view()),
    path('delete/<str:pk>',DeleteEventApiView.as_view()),
    path('inscription/',InscriptionEvenementView.as_view()),
    path('annulation-inscription/',AnnulationInscriptionView.as_view()),
    path('export/<str:id_evenement>',ExportParticipantsView.as_view())

]