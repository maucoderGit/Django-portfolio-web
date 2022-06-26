from django.http import HttpResponse
from django.urls import path
from . import views

app_name='main'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>:projects/', views.ProjectView.as_view(), name='project')
]
