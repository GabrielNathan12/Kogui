from django.db import models

# Create your models here.

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Form(models.Model):
    class Meta:
        model = Lead
        fields = ['nome', 'email']