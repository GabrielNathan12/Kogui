from django.urls import path
from .views import create_lead, success, dashboard, lead_list, delete_lead

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("create-lead/", create_lead, name='create_lead'),
    path("delete-lead/<int:pk>", delete_lead, name="delete_lead"),
    path("leads/", lead_list, name="lead_list"),
]