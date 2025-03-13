from django.shortcuts import redirect, render
import requests


API_URL = "http://127.0.0.1/agenda/"


def listar_agendas(request):
    response = requests.get(API_URL)    
    if response.status_code == 200:
        agendas = response.json()
    else:
        agendas = []

    return render(request, "webagenda/listar_agendas.html", {"agendas": agendas})


def criar_agenda(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        data = request.POST.get("data")
        descricao = request.POST.get("descricao")
        agenda_data = {"nome": nome, "data": data, "descricao": descricao}
        response = requests.post(API_URL, data=agenda_data)
        if response.status_code == 201:
            return redirect("listar_agendas")
    return render(request, "webagenda/criar_agenda.html")


def editar_agenda(request, id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        data = request.POST.get("data")
        descricao = request.POST.get("descricao")
        agenda_data = {"nome": nome, "data": data, "descricao": descricao}
        response = requests.put(f"{API_URL}{id}/", data=agenda_data)
        if response.status_code == 200:
            return redirect("listar_agendas")
    response = requests.get(f"{API_URL}{id}/")
    if response.status_code == 200:
        agenda = response.json()
    else:
        agenda = None
    return render(request, "webagenda/editar_agenda.html", {"agenda": agenda})


def deletar_agenda(request, id):
    if request.method == "POST":
        response = requests.delete(f"{API_URL}{id}/")
        if response.status_code == 204:
            return redirect("listar_agendas")
    return redirect("listar_agendas")