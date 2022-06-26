from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('main.urls')),
    path('', RedirectView.as_view(url='home/', permanent=False))
]
