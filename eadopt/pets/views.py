from django.shortcuts import render
from pets.models import Pet
from usuarios.models import Usuario
from django.contrib import messages
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
import django.utils.formats as fmt

def index(request):
    pets = list(Pet.objects.filter(dono_id=request.session['usuario_id']))
    return render(request, 'pets_do_usuario.html', { "pets":pets })

def novo(request):
    return redirect('pets_index')

def perfil(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    dono = Usuario.objects.get(id=pet.dono_id)
    return render(request, 'perfil_pet.html', {"pet":pet, "dono":dono})

def criar(request):
    novo_pet = preencher(request)
    novo_pet.save()
    db = conectar_mongo()
    sitedb = db.pets
    resultado = conectar_mongo().pets.insert_one({
        'id_postgres': novo_pet.id,
        'nome': novo_pet.nome,
        'descricao': request.POST['descricao']
        })
    novo_pet.id_mongo = str(resultado.inserted_id)
    novo_pet.save()
    print("OIiiiii")
    return redirect('pets_index')

def preencher(request):
    pet = Pet()
    pet.dono_id = request.session['usuario_id']
    pet.data_nascimento = request.POST['data_nascimento']
    pet.nome = request.POST['nome']
    pet.especie = request.POST['especie']

    return pet
