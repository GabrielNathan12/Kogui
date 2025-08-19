from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import Form
from .models import Lead

def dashboard(request):
    today = timezone.localdate()
    total_leads = Lead.objects.count()
    leads_today = Lead.objects.filter(created_at__date=today).count()
    recent_leads = Lead.objects.order_by('-created_at')[:3]
    
    return render(request, 'main/dashboard.html', {
        'total_leads': total_leads,
        'leads_today': leads_today,
        'recent_leads' : recent_leads
    })
    
def lead_list(request):
    query = request.GET.get("keyword", "").strip()
    leads = Lead.objects.order_by("-created_at")

    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company_name__icontains=query)
        )

    paginator = Paginator(leads, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    rows = [{"lead": l, "form": Form(instance=l)} for l in leads]
    
    return render(request, "main/list.html", {
        "leads": page_obj,
        "query": query,
        "page_obj": page_obj,
        "rows": rows
    })

def create_lead(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.save()
                messages.success(request, "Lead cadastrado com sucesso! ✅")
                return redirect('lead_list')
            except IntegrityError:
                form.add_error("email", "Este e-mail já está cadastrado.")
                messages.error(request, "Este e-mail já está cadastrado.")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = Form()

    return render(request, 'main/form.html', {'form': form})

def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        lead.delete()
        messages.success(request, "Lead excluído com sucesso")
        return redirect("lead_list")
    messages.error(request, "Operação inválida")
    
    return redirect("lead_list")

def edit_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = Form(request.POST, instance=lead)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Lead atualizado com sucesso! ✏️")
            except IntegrityError:
                messages.error(request, "Erro: já existe um lead com esse e-mail.")
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
        return redirect("lead_list")

    messages.error(request, "Requisição inválida.")
    return redirect("lead_list")
