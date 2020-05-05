from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/contact
    path('', views.index, name="contact")
]