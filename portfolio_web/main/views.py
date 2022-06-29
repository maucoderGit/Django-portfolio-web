from django import forms
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, TemplateView, DetailView

from main.models import Project, ProjectTag


class HomeView(ListView):
    """Home class-based view"""
    template_name: str = 'main/home.html'
    context_object_name: str = 'latest_projects_list'

    # Important! this is a overwrited method, the name must be equals
    def get_queryset(self) -> list[Project]:
        """
        Excludes any question that aren't published yet
        """
        return Project.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        

class ProjectView(DetailView):
    model = Project
    template_name: str = 'main/single_project.html'

    def get_queryset(self):
        """
        Excludes any question that aren't published yet
        """
        query_set = Project.objects.filter(pub_date__lte=timezone.now())

        for project in query_set:
            if len(project.tag_set.all()) <= 0:
                raise forms.ValidationError('At least one choice required.')
        return query_set

class ProjectsView(ListView):
    context_object_name: str = 'latest_projects_list'
    template_name: str = 'main/projects_page.html'

    def get_queryset(self):
        """
        Excludes any question that aren't published yet
        """    
        query_set = Project.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        for project in query_set:
            if len(project.tag_set.all()) <= 0:
                raise forms.ValidationError('At least one tag is required')
        return query_set