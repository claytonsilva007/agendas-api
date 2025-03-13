from datetime import datetime, timedelta
from django.shortcuts import redirect, render
import requests
from django import template
register = template.Library()


API_URL = "http://127.0.0.1/agenda/"


def listar_agendas(request):
    response = requests.get(API_URL)
    eventos = response.json() if response.status_code == 200 else []

    # Criar a estrutura do grid
    dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    horas_do_dia = [f"{h:02d}:{m:02d}" for h in range(0, 24) for m in [0, 15, 30, 45]]
    agenda_grid = {dia: {hora: [] for hora in horas_do_dia} for dia in dias_da_semana}

    # Preencher o grid com eventos
    for evento in eventos:
        data_inicio = datetime.strptime(evento["dataInicio"], "%Y-%m-%dT%H:%M:%SZ")
        data_fim = datetime.strptime(evento["dataFim"], "%Y-%m-%dT%H:%M:%SZ")

        # Verificar e corrigir o data_fim se for anterior ao data_inicio
        if data_fim <= data_inicio:
            data_fim = data_inicio + timedelta(minutes=15)

        nome_dia = data_inicio.strftime("%A")  # Nome do dia em inglês
        dia_semana = {
            "Monday": "Segunda", "Tuesday": "Terça", "Wednesday": "Quarta",
            "Thursday": "Quinta", "Friday": "Sexta"
        }.get(nome_dia, "")

        if dia_semana:
            hora_inicio = data_inicio.strftime("%H:%M")
            hora_fim = data_fim.strftime("%H:%M")

            # Preencher os horários entre início e fim
            tempo_atual = data_inicio
            while tempo_atual <= data_fim:
                hora_atual = tempo_atual.strftime("%H:%M")
                if hora_atual in agenda_grid[dia_semana]:
                    agenda_grid[dia_semana][hora_atual].append(evento)
                tempo_atual += timedelta(minutes=15)

    return render(request, "webagenda/listar_agendas.html", {
        "dias_da_semana": dias_da_semana,
        "horas_do_dia": horas_do_dia,
        "agenda_grid": agenda_grid,
    })


def gerenciar_agenda(request, id=None):
    if request.method == "POST":
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
            # Edição de agenda existente
            response = requests.put(f"{API_URL}{id}/", json=agenda_data, headers=headers)
            if response.status_code == 200:
                return redirect("listar_agendas")
        else:
            # Criação de nova agenda
            response = requests.post(API_URL, json=agenda_data, headers=headers)
            if response.status_code == 201:
                return redirect("listar_agendas")

    agenda = None
    
    if id:
        response = requests.get(f"{API_URL}{id}/")
        if response.status_code == 200:
            agenda = response.json()
            # Ajustar formato das datas para o campo datetime-local
            agenda['dataInicio'] = datetime.strptime(agenda['dataInicio'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M")
            agenda['dataFim'] = datetime.strptime(agenda['dataFim'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M")

    return render(request, "webagenda/gerenciar_agenda.html", {"agenda": agenda})



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
