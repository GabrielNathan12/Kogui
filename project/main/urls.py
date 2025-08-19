from django.urls import path
from .views import create_lead, dashboard, lead_list, delete_lead, edit_lead

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("create-lead/", create_lead, name='create_lead'),
    path("edit-lead/<int:pk>", edit_lead, name="edit_lead"),
    path("delete-lead/<int:pk>", delete_lead, name="delete_lead"),
    path("leads/", lead_list, name="lead_list"),
]