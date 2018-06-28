from django.shortcuts import render
from usuarios.models import Usuario, PF, PJ
from visitas.models import Visita
from pets.models import Pet
from django.contrib import messages
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
import django.utils.formats as fmt

def index(request):
    if (request.session['tipo'] == "pf"):
        usuario = PF.objects.get(id=request.session["usuario_id"])
    else:
        usuario = PJ.objects.get(id=request.session["usuario_id"])

    visitas = list(Visita.objects.filter(visitante_id=request.session["usuario_id"]))


    return render(request, 'visita_index.html', {"usuario":usuario, "visitas":visitas})

def criar(request):
    pets = list(Pet.objects.all())
    dono = {}
    for pet in pets:
        dono[pet.nome] = Usuario.objects.get(id=pet.dono.id).nome

    if (request.session['tipo'] == "pf"):
        usuario = PF.objects.get(id=request.session["usuario_id"])
    else:
        usuario = PJ.objects.get(id=request.session["usuario_id"])


    return render(request, 'visita_criar.html', {"usuario":usuario, "pets": pets})

def convidar(request):
    visita_nova = preencher(request)
    visita_nova.save()
    return redirect('visitas_index')

def remover(request, visita_id):
    visita = Visita.objects.get(id=visita_id)
    visita.delete()
    return redirect('visitas_index')



def preencher(request):
    visita = Visita()
    visita.visitante = Usuario.objects.get(id=request.session["usuario_id"])
    pet = Pet.objects.get(id=request.POST["pet"])
    visita.pet = pet
    visita.data_hora = request.POST["data_hora"]
    visita.comentario = request.POST["comentario"]
    return visita
