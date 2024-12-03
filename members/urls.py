from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',SignUpView.as_view()),
    path('signin/',SignInView.as_view()),
    path('members/',ListMemberApiView.as_view()),
    path('members/<str:id_membre>',RetrieveMemberByIdApiView.as_view()),
    path("members/delete/<str:pk>",DeleteMemberApiView.as_view()),
    path('members/update/<str:pk>',UpdateMemberApiView.as_view()),


    #endpoints de cotisation:
    path('cotisation/',ListCotisationApiView.as_view()),
    path('cotisation/<str:id_cotisation>',RetrieveCotisationByIdApiView.as_view()),
    path("cotisation/delete/<str:pk>",DeleteCotisationApiView.as_view()),
    path('cotisation/update/<str:pk>',UpdateCotisationApiView.as_view()),
    path('cotisation/register/',CreateCotisationApiView.as_view()),
]
