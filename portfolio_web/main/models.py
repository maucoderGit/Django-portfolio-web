from datetime import datetime, timedelta
from django import forms
from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Project(models.Model):
    title: str = models.CharField(max_length=50)
    headline: str = models.CharField(max_length=150)
    content_text: str = models.TextField()
    pub_date: datetime = models.DateTimeField("date_published")

    def __str__(self):
        """Returns a attribute in string type"""
        return self.title

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?'
    )
    def was_published_recently(self) -> bool:
        """
        Validate if a question was published recently (Not more to seven days).
        Returns True if was published recently.
        """
        return timezone.now() >= self.pub_date >= timezone.now() - timedelta(days=1)

# Tags
class Tag(models.Model):
    tag_name: str = models.CharField(max_length=35)
    tags_projects: Project = models.ManyToManyField(Project, through="ProjectTag")

    def __str__(self):
        """Returns a attribute in string type"""
        return self.tag_name

class ProjectTag(models.Model):
    tag_fk = models.ForeignKey(Tag, verbose_name=(""), on_delete=models.CASCADE)
    project_fk = models.ForeignKey(Project, verbose_name=(""), on_delete=models.CASCADE)