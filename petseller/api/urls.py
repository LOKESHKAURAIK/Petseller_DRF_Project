from django.urls import path
from home.views import *
urlpatterns = [
    path('animals/', AnimalView.as_view()),
    path('animal_increment/<pk>/', AnimalDetailView.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),

]
