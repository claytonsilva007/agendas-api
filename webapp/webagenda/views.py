from datetime import datetime, timedelta
from django.shortcuts import redirect, render
import requests
from django import template
import pytz
from webagenda.models import EstadoAgenda
from django.contrib.auth.decorators import login_required

from webagenda.api_client import APIClient

register = template.Library()

@login_required
def listar_agendas(request):
    semana_offset = int(request.GET.get("semana_offset", 0))

    hoje = datetime.today().astimezone(pytz.utc)
    inicio_semana = (hoje - timedelta(days=hoje.weekday()) + timedelta(weeks=semana_offset)).replace(hour=0, minute=0, second=0, microsecond=0)
    fim_semana = inicio_semana + timedelta(days=6, hours=23, minutes=59, seconds=59)

    eventos = APIClient.get("") or []  # Obtém eventos autenticados

    dias_da_semana = []
    data_referencia = inicio_semana
    
    while data_referencia <= fim_semana:
        if data_referencia.weekday() < 5:
            dias_da_semana.append({
                "nome": data_referencia.strftime("%A"),
                "data": data_referencia.strftime("%d"),
                "data_completa": data_referencia.strftime("%Y-%m-%d")
            })
        data_referencia += timedelta(days=1)

    horas_do_dia = [f"{h:02d}:00" for h in range(7, 24)]
    agenda_grid = {dia["nome"]: {hora: [] for hora in horas_do_dia} for dia in dias_da_semana}

    for evento in eventos:
        data_inicio = datetime.strptime(evento["dataInicio"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
        data_fim = datetime.strptime(evento["dataFim"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)

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


@login_required
def gerenciar_agenda(request, id=None):
    hora_param = request.POST.get("dateTime", None)  # Captura o parâmetro hora do POST

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

        if id:
            response = APIClient.put(f"{id}/", agenda_data)
            if response:
                return redirect("listar_agendas")
        else:
            response = APIClient.post("", agenda_data)
            if response:
                return redirect("listar_agendas")

    agenda = None
    
    if id:
        response = APIClient.get(f"{id}/")
        if response:
            agenda = response
            
            # Ajustar formato das datas para string compatível com input datetime-local
            agenda['dataInicio'] = datetime.strptime(agenda['dataInicio'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M")
            agenda['dataFim'] = datetime.strptime(agenda['dataFim'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M")
    
    if hora_param:
        agenda = {}
        # Adiciona ":00Z" ao formato da string para compatibilidade
        hora_param = f"{hora_param}:00Z"

        data_inicio = datetime.strptime(hora_param, "%Y-%m-%d %H:%M:%SZ")
        agenda['dataInicio'] = data_inicio.strftime("%Y-%m-%dT%H:%M")
        
        data_fim = data_inicio + timedelta(minutes=30)
        agenda['dataFim'] = data_fim.strftime("%Y-%m-%dT%H:%M")
        
        agenda['estado_atual'] = EstadoAgenda.RECEBIDO
        
    context = {"agenda": agenda}

    return render(request, "webagenda/gerenciar_agenda.html", context)


@login_required
def deletar_agenda(request, id):
    if request.method == "POST":
        success = APIClient.delete(f"{id}/")
        if success:
            return redirect("listar_agendas")
    return redirect("listar_agendas")


@register.filter
def dict_get(d, key):
    """Retorna o valor do dicionário usando a chave"""
    return d.get(key, None)