from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import requests  
import json
from datetime import datetime
from django.db.models import Q, Count
import requests
from hardware.models import Hardware
from .models import Job, Servidores_CC, Servidores_FastShop

def get_ping(url):
    try:
        response = requests.get(url, timeout=5)
        ping_time = response.elapsed.total_seconds() * 1000
        return f"{ping_time:.2f} ms"
    except requests.exceptions.RequestException:
        return "Inativo"

def index(request):
    return render(request, 'index.html')

@login_required
def search_jobs(request):
    # Obtém a consulta de pesquisa
    search_query = request.POST.get('search_query', '').strip() if request.method == 'POST' else ''

    # Filtra Jobs
    jobs = Job.objects.filter(
        Q(nome_job__icontains=search_query) | 
        Q(stream_job__icontains=search_query) | 
        Q(estacao_trabalho__icontains=search_query) |
        Q(aplicacao__icontains=search_query)
    ) if search_query else Job.objects.none()

    # Filtra Servidores CC
    servidores_cc = Servidores_CC.objects.filter(
        Q(server_name__icontains=search_query) | 
        Q(server_cliente__icontains=search_query) | 
        Q(ip__icontains=search_query)
    ) if search_query else Servidores_CC.objects.none()

    # Filtra Servidores FastShop
    servidores_fastshop = Servidores_FastShop.objects.filter(
        Q(server_name__icontains=search_query) | 
        Q(server_cliente__icontains=search_query) | 
        Q(ip__icontains=search_query)
    ) if search_query else Servidores_FastShop.objects.none()

    hardware_queryset = Hardware.objects.filter(  
        Q(marca__icontains=search_query) | 
        Q(modelo__icontains=search_query) | 
        Q(serial_number__icontains=search_query) | 
        Q(descricao__icontains=search_query) | 
        Q(local__icontains=search_query) | 
        Q(fornecedor_manut__icontains=search_query) | 
        Q(status_contrato__icontains=search_query) |
        Q(alerta__icontains=search_query)
    ) if search_query else Hardware.objects.none()



    # Mensagem se não houver resultados
    message = ""
    if not (servidores_cc or servidores_fastshop or jobs):
        message = "No results found for your search."

    # Retorna o template com os resultados
    return render(request, 'jobs/index.html', {
        'Servidores_FastShop': servidores_fastshop,
        'Servidores_CC': servidores_cc,
        'jobs': jobs,
        'hardware': hardware_queryset,
        'message': message,
    })


@login_required
def hardware(request):
    hardware_queryset = Hardware.objects.all()


    num_display = request.GET.get('num_display', 5)
    paginator = Paginator(hardware_queryset, int(num_display))

    page_number = request.GET.get('page')
    hardware_page = paginator.get_page(page_number)

    return render(request, 'jobs/index.html', {
        'hardware': hardware_page,  
        'num_display': num_display,
    })





@login_required
def show_all_jobs(request):
    jobs = Job.objects.all()


    num_display = request.GET.get('num_display', 5)
    paginator = Paginator(jobs, int(num_display))

    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    return render(request, 'jobs/index.html', {
        'jobs': jobs_page,
        'num_display': num_display,
    })

@login_required
def show_all_servers(request):
    servidores_cc = Servidores_CC.objects.all()  

    num_display = request.GET.get('num_display', 5)
    paginator = Paginator(servidores_cc, int(num_display))

    page_number = request.GET.get('page')
    servers_page = paginator.get_page(page_number)

    return render(request, 'jobs/index.html', {
        'Servidores_CC': servers_page,
        'num_display': num_display,
        'jobs': [],  
        'message': "",  
})
@login_required
def ajuda(request):
    return render(request, 'jobs/ajuda.html')


@login_required
def show_all_fastshop(request):
    servidores_fastshop = Servidores_FastShop.objects.all()  

    num_display = request.GET.get('num_display', 5)
    paginator = Paginator(servidores_fastshop, int(num_display))

    page_number = request.GET.get('page')
    fastshop_page = paginator.get_page(page_number)

    return render(request, 'jobs/index.html', {
        'Servidores_FastShop': fastshop_page,
        'num_display': num_display,
        'jobs': [],  
        'message': "",  
 })




@login_required
def dashboard(request):
    # Servidores ativos/inativos
    total_servidores_cc = Servidores_CC.objects.count()
    servidores_cc_ativos = Servidores_CC.objects.filter(is_active=True).count()
    servidores_cc_inativos = total_servidores_cc - servidores_cc_ativos
    
    total_servidores_fastshop = Servidores_FastShop.objects.count()
    servidores_fs_ativos = Servidores_FastShop.objects.filter(is_active=True).count()
    servidores_fs_inativos = total_servidores_fastshop - servidores_fs_ativos

    # Status dos Jobs
    total_jobs = Job.objects.count()
    jobs_por_criticidade = Job.objects.values('criticality').annotate(total=Count('id'))
    jobs_por_workstation = Job.objects.values('estacao_trabalho').annotate(total=Count('id'))
    jobs_por_aplicacao = Job.objects.values('aplicacao').annotate(total=Count('id'))

    # Hardwares
    hardwares_por_status = Hardware.objects.values('status_contrato').annotate(total=Count('id'))
    hardwares_alertas = Hardware.objects.exclude(alerta='unknown').count()
    hardwares_em_manutencao = Hardware.objects.filter(status_contrato__icontains='manutencao').count()

    # Realizar múltiplas medições de ping
    for _ in range(10):
        get_ping("http://127.0.0.1:8000/")

    # Contexto com dados reais
    context = {
        'servidores_cc': {
            'total': total_servidores_cc,
            'ativos': servidores_cc_ativos,
            'inativos': servidores_cc_inativos
        },
        'servidores_fastshop': {
            'total': total_servidores_fastshop,
            'ativos': servidores_fs_ativos,
            'inativos': servidores_fs_inativos
        },
        'jobs': {
            'total': total_jobs,
            'por_criticidade': jobs_por_criticidade,
            'por_workstation': jobs_por_workstation,
            'por_aplicacao': jobs_por_aplicacao
        },
        'hardware': {
            'por_status': hardwares_por_status,
            'alertas': hardwares_alertas,
            'em_manutencao': hardwares_em_manutencao
        }
    }

    return render(request, 'jobs/dashboard.html', context)