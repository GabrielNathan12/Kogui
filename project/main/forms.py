import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Lead

class Form(forms.ModelForm):
    phone = forms.CharField(
        label="Telefone",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "id": "id_phone"
        }),
    )

    class Meta:
        model = Lead
        fields = [
            "name", "email", "phone", "position", "company_name",
            "segment", "company_size", "main_interest",
            "follow_up", "observations",
        ]
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "position": "Cargo",
            "company_name": "Nome da empresa",
            "segment": "Segmento",
            "company_size": "Tamanho da empresa",
            "main_interest": "Principal interesse",
            "follow_up": "Follow-up",
            "observations": "Observações",
        }
        help_texts = {
            "email": "Use um e-mail válido. Duplicados não são permitidos.",
        }
        error_messages = {
            "email": {
                "invalid": "Informe um endereço de email válido.",
                "unique": "Este e-mail já está cadastrado.",
                "required": "O campo e-mail é obrigatório.",
            },
            "name": {"required": "O campo nome é obrigatório."},
            "phone": {"required": "O campo telefone é obrigatório."},
            "position": {"required": "O campo cargo é obrigatório."},
            "company_name": {"required": "O campo nome da empresa é obrigatório."},
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "segment": forms.Select(attrs={"class": "form-select"}),
            "company_size": forms.Select(attrs={"class": "form-select"}),
            "main_interest": forms.Select(attrs={"class": "form-select"}),
            "follow_up": forms.TextInput(attrs={"class": "form-control"}),
            "observations": forms.Textarea(attrs={"class": "form-control", "rows": 1}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        qs = Lead.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    
    def clean_phone(self):
        raw = self.cleaned_data.get("phone", "") or ""
        digits = re.sub(r"\D", "", raw)
        if not (8 <= len(digits) <= 20):
            raise ValidationError("Informe um telefone válido (apenas números, com DDD).")
        return digits
