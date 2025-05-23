from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import requests  
import json
from datetime import datetime
from django.db.models import Q
from hardware.models import Hardware
from .models import Job, Servidores_CC, Servidores_FastShop
@login_required
def search_jobs(request):
    # Obtém a consulta de pesquisa
    search_query = request.POST.get('search_query', '').strip() if request.method == 'POST' else ''

    # Filtra Jobs
    jobs = Job.objects.filter(
        Q(job_name__icontains=search_query) | 
        Q(job_stream__icontains=search_query) | 
        Q(workstation__icontains=search_query)
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
    # Contar total de usuários e servidores
    total_users = User.objects.count()
    total_servidores_cc = Servidores_CC.objects.count()
    total_servidores_fastshop = Servidores_FastShop.objects.count()
    total_jobs = Job.objects.count()

    # Função para obter o tempo de ping
    ping_times = []
    timestamps = []

    def get_ping(url):
        try:
            response = requests.get(url, timeout=5)
            ping_time = response.elapsed.total_seconds() * 1000
            ping_times.append(ping_time)
            timestamps.append(datetime.now().strftime("%H:%M:%S"))  # Adiciona timestamp
            return f"{ping_time:.2f} ms"
        except requests.exceptions.RequestException:
            return "Inativo"

    # Realizar múltiplas medições de ping
    for _ in range(10):
        get_ping("http://127.0.0.1:8000/")

    # Contexto para renderização do template
    context = {
        'total_users': total_users,
        'total_servidores_cc': total_servidores_cc,
        'total_servidores_fastshop': total_servidores_fastshop,
        'total_jobs': total_jobs,
        'ping_result': f"{ping_times[-1]:.2f} ms" if ping_times else "Inativo",
        'ping_times_json': json.dumps(ping_times),  # Passa tempos de ping como JSON
        'timestamps_json': json.dumps(timestamps),  # Passa timestamps como JSON
        'users_data': [total_users] * 10,
        'serv_cc_data': [total_servidores_cc] * 10,
        'serv_fastshop_data': [total_servidores_fastshop] * 10,
        'jobs_data': [total_jobs] * 10,
    }

    return render(request, 'jobs/dashboard.html', context)