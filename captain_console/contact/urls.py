from django.urls import path
from . import views
from .views import contactView, successView

urlpatterns = [
    # http://localhost:8000/contact
    path('', contactView, name="contact"),
    path('success/', successView, name='success')
]