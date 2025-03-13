from datetime import datetime, timedelta
from django.shortcuts import redirect, render
import requests
from django import template
register = template.Library()


API_URL = "http://127.0.0.1/agenda/"


def listar_agendas(request):
    # Captura o deslocamento de semanas a partir da URL (ex: ?semana_offset=1)
    semana_offset = int(request.GET.get("semana_offset", 0))

    # Define o início da semana baseada no deslocamento
    hoje = datetime.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday()) + timedelta(weeks=semana_offset)
    fim_semana = inicio_semana + timedelta(days=6)

    response = requests.get(API_URL)
    eventos = response.json() if response.status_code == 200 else []

    # Criar estrutura do grid com horas inteiras
    dias_da_semana = []
    data_referencia = inicio_semana
    
    while data_referencia <= fim_semana:
        # Adiciona apenas dias úteis (segunda a sexta-feira)
        if data_referencia.weekday() < 5:  # 0 = segunda-feira, 1 = terça-feira, ..., 4 = sexta-feira
            dias_da_semana.append({
                "nome": data_referencia.strftime("%A"),
                "data": data_referencia.strftime("%d"),
                "data_completa": data_referencia.strftime("%Y-%m-%d")
            })
        
        data_referencia += timedelta(days=1)

    horas_do_dia = [f"{h:02d}:00" for h in range(7, 24)]  # Apenas horas inteiras
    agenda_grid = {dia["nome"]: {hora: [] for hora in horas_do_dia} for dia in dias_da_semana}

    # Filtrar e preencher a agenda com eventos da semana
    for evento in eventos:
        data_inicio = datetime.strptime(evento["dataInicio"], "%Y-%m-%dT%H:%M:%SZ")
        data_fim = datetime.strptime(evento["dataFim"], "%Y-%m-%dT%H:%M:%SZ")

        # Verificar se o evento pertence à semana atual
        if inicio_semana <= data_inicio <= fim_semana:
            nome_dia = data_inicio.strftime("%A")
            hora_inicio = data_inicio.strftime("%H:00")

            if nome_dia in agenda_grid and hora_inicio in agenda_grid[nome_dia]:
                agenda_grid[nome_dia][hora_inicio].append(evento)

    return render(request, "webagenda/listar_agendas.html", {
        "dias_da_semana": dias_da_semana,
        "horas_do_dia": horas_do_dia,
        "agenda_grid": agenda_grid,
        "semana_offset": semana_offset,
        "mes_atual": inicio_semana.strftime("%B de %Y"),
        "data_hoje": hoje.strftime("%d/%m/%Y"),
    })

    

def _round_time(dt):
    minutes = (dt.minute // 15) * 15
    return dt.replace(minute=minutes, second=0, microsecond=0)


def gerenciar_agenda(request, id=None):
    hora_param = request.POST.get("hora", None)  # Captura o parâmetro hora do POST

    if request.method == "POST" and not hora_param:
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        dataInicio = request.POST.get("dataInicio")
        dataFim = request.POST.get("dataFim")
        local = request.POST.get("local")
        estado_atual = request.POST.get("estado_atual")

        agenda_data = {
            "titulo": titulo,
            "descricao": descricao,
            "dataInicio": dataInicio,
            "dataFim": dataFim,
            "local": local,
            "estado_atual": estado_atual
        }

        headers = {"Content-Type": "application/json"}

        if id:
            response = requests.put(f"{API_URL}{id}/", json=agenda_data, headers=headers)
            if response.status_code == 200:
                return redirect("listar_agendas")
        else:
            response = requests.post(API_URL, json=agenda_data, headers=headers)
            if response.status_code == 201:
                return redirect("listar_agendas")

    agenda = None
    
    if id:
        response = requests.get(f"{API_URL}{id}/")
        if response.status_code == 200:
            agenda = response.json()
            
            # Ajustar formato das datas para string compatível com input datetime-local
            agenda['dataInicio'] = datetime.strptime(agenda['dataInicio'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M")
            agenda['dataFim'] = datetime.strptime(agenda['dataFim'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M")

    context = {"agenda": agenda}
    if hora_param:
        context['hora_param'] = hora_param  # Adiciona hora_param ao contexto

    return render(request, "webagenda/gerenciar_agenda.html", context)



def deletar_agenda(request, id):
    if request.method == "POST":
        response = requests.delete(f"{API_URL}{id}/")
        if response.status_code == 204:
            return redirect("listar_agendas")
    return redirect("listar_agendas")


@register.filter
def dict_get(d, key):
    """Retorna o valor do dicionário usando a chave"""
    return d.get(key, None)
