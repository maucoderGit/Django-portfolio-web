from django.shortcuts import render

# Create your views here.

def home_view(response):
    """
    Response with the template home.html
    """
    return render(response, 'home.html')