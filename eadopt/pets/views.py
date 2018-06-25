from django.shortcuts import render
from usuarios.models import Usuario, PF, PJ
from django.contrib import messages
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
import django.utils.formats as fmt

def index(request):
    return render(request, 'pets_do_usuario.html')

def novo(request):
    return render(request, 'novo.html')


def criar(request):
    novo_pet = preencher(request)
    novo_pet.save()
    resultado = conectar_mongo().pets.insert_one({
        'id_postgres': novo_pet.id,
        'nome': novo_pet.nome
        })
    novo_pet.id_mongo = str(resultado.inserted_id)
    novo_pet.save()
    return redirect('index')

    def preencher(request):
        pet = Pet()
        pet.data_nascimento = request.POST['data_nascimento']
        pet.nome = request.POST['nome']
        pet.especie = request.POST['especie']
