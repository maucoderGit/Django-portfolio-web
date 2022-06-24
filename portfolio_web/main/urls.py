from django.urls import path
from . import views

app_name='main'
urlpatterns = [
    path('home/', view=views.home_view, name='main'),
]
