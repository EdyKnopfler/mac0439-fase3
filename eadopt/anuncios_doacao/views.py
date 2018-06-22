from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from pets.models import Pet
from anuncios_doacao.models import AnuncioDoacao
from eadopt.mongo import conectar_mongo


def index(request):
    meus_pets = Pet.objects.filter(dono_id=request.session['usuario_id'])
    meus_anuncios = AnuncioDoacao.objects.filter(pet__in=meus_pets)
    return render(request, 'anuncios/index.html', {'meus_anuncios':meus_anuncios})

    
def novo(request):
    pets = Pet.objects.filter(dono_id=request.session['usuario_id'])
    return render(request, 'anuncios/novo.html', {'pets':pets})
    
    
def criar(request):
    novo_anuncio = preencher(AnuncioDoacao(), request)
    novo_anuncio.save()
    resultado = conectar_mongo().anuncios.insert_one({
        'id_postgres': novo_anuncio.id,
        'descricao': request.POST['descricao']
    })
    novo_anuncio.id_mongo = str(resultado.inserted_id)
    novo_anuncio.save()
    return redirect('anuncio_index')
    
    
def editar(request, anuncio_id):
    pets = Pet.objects.filter(dono_id=request.session['usuario_id'])
    anuncio = AnuncioDoacao.objects.get(id=anuncio_id)
    doc = conectar_mongo().anuncios.find_one({"_id": ObjectId(anuncio.id_mongo)})
    return render(request, 'anuncios/novo.html', {'pets': pets, 'anuncio':anuncio, 'descricao':doc['descricao']})
    
    
def preencher(anuncio, request):
    agora = datetime.date(datetime.now())
    anuncio.data_inicio = request.POST['data_inicio'] if request.POST['data_inicio'] != '' else agora
    daqui_um_mes = agora + timedelta(days=30)
    anuncio.data_termino = request.POST['data_termino'] if request.POST['data_termino'] != '' else daqui_um_mes
    anuncio.pet_id = request.POST['pet_id']
    return anuncio

