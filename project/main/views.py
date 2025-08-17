from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from .forms import Form
from .models import Lead

def dashboard(request):
    today = timezone.localdate()
    total_leads = Lead.objects.count()
    leads_today = Lead.objects.filter(created_at__date=today).count()
    
    return render(request, 'main/dashboard.html', {
        'total_leads': total_leads,
        'leads_today': leads_today
    })
    
def lead_list(request):
    leads = Lead.objects.order_by("-created_at")
    return render(request, "list.html", {"leads": leads})


def home(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Lead cadastrado com sucesso! ✅")
                return redirect('success')
            except IntegrityError:
                form.add_error("email", "Este e-mail já está cadastrado.")
                messages.error(request, "Este e-mail já está cadastrado.")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = Form()

    return render(request, 'main/form.html', {'form': form})

def success(request):
    return render(request, 'main/success.html')
