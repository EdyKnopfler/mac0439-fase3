from django.shortcuts import render
from usuarios.models import Usuario, PF, PJ
from visitas.models import Visita
from pets.models import Pet
from django.contrib import messages
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
from django.db.models import Q
from django.http import HttpResponse
import django.utils.formats as fmt
import json

def get_pets_names(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        nomes = Pet.objects.filter(Q(nome__icontains = q))[:10]
        results = []
        for n in nomes:
            info = {}
            info['label'] = n.nome + " (" + n.dono.nome + " - " + n.dono.email + ")" + " " + str(n.id)
            info['id'] = n.id
            results.append(info)
        data = json.dumps(results)
    else:
        data = 'fail'
    # print(data)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def index(request):
    if (request.session['tipo'] == "pf"):
        usuario = PF.objects.get(id=request.session["usuario_id"])
    else:
        usuario = PJ.objects.get(id=request.session["usuario_id"])

    visitas = list(Visita.objects.filter(visitante_id=request.session["usuario_id"]))

    pets = list(Pet.objects.filter(dono_id=request.session["usuario_id"]))
    convites = {}

    for p in pets:
        convites[p.nome] = list(Visita.objects.filter(pet_id=p.id))

    #for convidado, convite in convites.items():
    #    for c in convite:
    #        print (c.pet.nome)

    return render(request, 'visita_index.html', {"usuario":usuario, "visitas":visitas, "convites":convites})

def criar(request):
    pets = list(Pet.objects.all())
    donos = list(Usuario.objects.all())

    if (request.session['tipo'] == "pf"):
        usuario = PF.objects.get(id=request.session["usuario_id"])
    else:
        usuario = PJ.objects.get(id=request.session["usuario_id"])


    return render(request, 'visita_criar.html', {"usuario":usuario, "pets": pets, "donos":donos})

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
    pet = request.POST["pet"]
    infopet = pet.split( )
    objpet = Pet.objects.get(id=infopet[-1])
    #objpet = request.POST["pet"]
    visita.pet = objpet
    visita.data_hora = request.POST["data"] + "T" + request.POST["hora"]
    visita.comentario = request.POST["comentario"]
    return visita
