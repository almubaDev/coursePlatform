from django.shortcuts import render

def home_view(request):
    """Vista para la página de inicio"""
    return render(request, 'home/index.html')