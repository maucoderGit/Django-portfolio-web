from django import forms
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, TemplateView, DetailView

from main.models import Project


class HomeView(ListView):
    """Home class-based view"""
    template_name: str = 'main/home.html'
    context_object_name: str = 'latest_projects_list'

    # Important! this is a overwrited method, the name must be equals
    def get_queryset(self) -> list[Project]:
        """
        Excludes any question that aren't published yet
        """
        return Project.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:6]
        
class ProjectView(ListView):
    """Project detail class-based view"""
    model = Project
    template_name: str = 'main/base.html'