from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Lead

phone_validator = RegexValidator(
    regex=r"^\+?\d{8,20}$",
    message="Informe um telefone válido (somente dígitos, com DDD e opcional +DDI).",
)

class Form(forms.ModelForm):
    phone = forms.CharField(
        label="Telefone",
        max_length=20,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={"placeholder": "+55DDDXXXXXXXXX"}),
    )

    class Meta:
        model = Lead
        fields = [
            "name", "email", "phone", "position", "company_name",
            "segment", "company_size", "main_interest",
            "follow_up", "observations",
        ]
        widgets = {
            "segment": forms.Select(),
            "company_size": forms.Select(),
            "main_interest": forms.Select(),
            "observations": forms.Textarea(attrs={"rows": 3}),
        }
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

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if Lead.objects.filter(email__iexact=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email
