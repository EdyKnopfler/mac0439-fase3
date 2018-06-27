from django.shortcuts import render
from pets.models import Pet, Foto
from usuarios.models import Usuario
from django.contrib import messages
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
import django.utils.formats as fmt
from django.core.files.storage import FileSystemStorage
import sys
import os

def index(request):
    pets = list(Pet.objects.filter(dono_id=request.session['usuario_id']))
    return render(request, 'pets_do_usuario.html', { "pets":pets })

def novo(request):
    return render(request, 'novo_pet.html')

def editar(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    descricao = conectar_mongo().pets.find_one({"_id": ObjectId(pet.id_mongo)})
    pet.descricao = descricao["descricao"]
    request.session['pet_mongo_id'] = pet.id_mongo
    request.session['pet_id'] = pet.id
    return render (request, 'editar_pet.html', {"pet": pet})

def atualizar(request):
    pet = preencher(request)
    pet.id = request.session["pet_id"]
    pet.id_mongo = request.session['pet_mongo_id']
    pet.save()
    try:
        fotos = request.FILES.getlist('arquivo')
        fs = FileSystemStorage()
        for arqv in fotos:
            filename, file_extension =  os.path.splitext(arqv.name)
            filename = fs.save(
                str(request.session['usuario_id']) + "_" + str(pet.id) + file_extension, arqv)
            foto = Foto()
            foto.pet_id = pet.id
            foto.arquivo = filename
            foto.save()
    except Exception:
        e = sys.exc_info()
        print("erro!")
        print(e)
    conectar_mongo().pets.update_one({"_id": ObjectId(request.session['pet_mongo_id'])}, {
        "$set": {'nome':request.POST['nome'], 'descricao': request.POST['descricao']}
    })
    return redirect ('pets_index')

def remover(request):
    return Oi

def perfil(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    dono = Usuario.objects.get(id=pet.dono_id)
    fotos = Foto.objects.filter(pet_id = pet.id)
    return render(request, 'perfil_pet.html', {"pet":pet, "dono":dono, "fotos":fotos})

def criar(request):
    novo_pet = preencher(request)
    novo_pet.save()
    try:
        fotos = request.FILES.getlist('arquivo')
        fs = FileSystemStorage()
        for arqv in fotos:
            filename, file_extension =  os.path.splitext(arqv.name)
            filename = fs.save(
                str(request.session['usuario_id']) + "_" + str(novo_pet.id) + file_extension, arqv)
            foto = Foto()
            foto.pet_id = novo_pet.id
            foto.arquivo = filename
            foto.save()
    except Exception:
        e = sys.exc_info()
        print("erro!")
        print(e)
    db = conectar_mongo()
    sitedb = db.pets
    resultado = conectar_mongo().pets.insert_one({
        'id_postgres': novo_pet.id,
        'nome': novo_pet.nome,
        'descricao': request.POST['descricao']
        })
    novo_pet.id_mongo = str(resultado.inserted_id)
    novo_pet.save()
    return redirect('pets_index')

def preencher(request):
    pet = Pet()
    pet.dono_id = request.session['usuario_id']
    pet.data_nascimento = request.POST['data_nascimento']
    pet.nome = request.POST['nome']
    pet.especie = request.POST['especie']
    pet.descricao = request.POST['descricao']
    return pet
