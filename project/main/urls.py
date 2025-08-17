from django.urls import path
from .views import home, success, dashboard, lead_list

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("leads/", lead_list, name="lead-list"),
    path('success/', success, name='success'),

]