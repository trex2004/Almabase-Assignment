from django.urls import path
from app.api.viewsets.contact import CreateContact

urlpatterns = [
    path('contact', CreateContact.as_view(), name='contact-create'),
]
