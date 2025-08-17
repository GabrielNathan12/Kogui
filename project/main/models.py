from django.db import models

# Create your models here.

class Lead(models.Model):
    SEGMENT_CHOICES = [
        ("tech", "Tecnologia"),
        ("fin", "Financeiro"),
        ("edu", "Educação"),
        ("ind", "Indústria"),
        ("outros", "Outros"),
    ]
    
    COMPANY_SIZE_CHOICES = [
        ("1-10", "1–10"),
        ("11-50", "11–50"),
        ("51-200", "51–200"),
        ("201-500", "201–500"),
        ("500+", "500+"),
    ]
    
    MAIN_INTEREST_CHOICES = [
        ("site", "Site institucional"),
        ("app", "Aplicativo"),
        ("ecom", "E-commerce"),
        ("integr", "Integrações/Automação"),
        ("consult", "Consultoria"),
        ("outros", "Outros"),
    ]
    
    name = models.CharField("Nome", max_length=100)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField("Telefone", max_length=20, default="")
    position = models.CharField("Cargo", max_length=100, default="") 
    company_name = models.CharField("Nome da empresa", max_length=150, default="")
    
    segment = models.CharField("Segmento", max_length=20, choices=SEGMENT_CHOICES, blank=True)
    company_size = models.CharField("Tamanho da empresa", max_length=10, choices=COMPANY_SIZE_CHOICES, blank=True)
    main_interest = models.CharField("Principal interesse", max_length=12, choices=MAIN_INTEREST_CHOICES, blank=True)
    follow_up = models.CharField("Como soube/Follow-up", max_length=200, blank=True)
    observations = models.TextField("Observações", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} <{self.email}>"