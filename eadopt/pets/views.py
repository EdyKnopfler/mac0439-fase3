from django.shortcuts import render
from pets.models import Pet, Foto
from usuarios.models import Usuario
from visitas.models import Visita
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
    chave_valor = {}
    return render(request, 'novo_pet.html', {"ChaveValor":chave_valor})

def editar(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    mongo_pet = conectar_mongo().pets.find_one({"_id": ObjectId(pet.id_mongo)})
    pet.descricao = mongo_pet["descricao"]
    request.session['pet_mongo_id'] = pet.id_mongo
    request.session['pet_id'] = pet.id
    fotos = Foto.objects.filter(pet_id = pet.id)
    return render (request, 'editar_pet.html', {"pet": pet, "fotos":fotos, 'ficha':mongo_pet["ficha"]})

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
    
    ficha = set(request.POST.getlist('chavevalor'))
    ficha_texto = ''
    for cada_campo in ficha:
        ficha_texto += cada_campo + '; '
    pets = conectar_mongo().pets
    id_mongo = ObjectId(request.session['pet_mongo_id'])
    conectar_mongo().pets.update_one({"_id": id_mongo}, {
        "$set": {'nome':request.POST['nome'], 'descricao':request.POST['descricao'], 'ficha':[], 'ficha_texto':ficha_texto}
    })
    for cada_campo in ficha:
        ChaveValor = cada_campo.split(":")
        pets.update({ '_id': id_mongo}, {'$push':{'ficha': {ChaveValor[0]: ChaveValor[1]}}})
    return redirect ('pets_index')

def remover(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    conectar_mongo().pets.delete_one({"_id": ObjectId(pet.id_mongo)})
    fotos = list(Foto.objects.filter(pet = pet))
    for foto in fotos:
        foto.delete()
    visitas = list(Visita.objects.filter(pet = pet))
    for visita in visitas:
        visita.delete()
    pet.delete()

    return redirect('pets_index')

def perfil(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    dono = Usuario.objects.get(id=pet.dono_id)
    mongo_pet = conectar_mongo().pets.find_one({"_id": ObjectId(pet.id_mongo)})
    pet.descricao = mongo_pet["descricao"]
    fotos = Foto.objects.filter(pet_id = pet.id)
    for chave, valor in mongo_pet["ficha"][0].items():
        print (chave)
        print (valor)
    return render(request, 'perfil_pet.html', {"pet":pet, "dono":dono, "fotos":fotos, "ficha":mongo_pet["ficha"]})

def criar(request):
    novo_pet = preencher(request)
    novo_pet.save()
    ficha = set(request.POST.getlist('chavevalor'))

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
    ficha_texto = ''
    for cada_campo in ficha:
        ficha_texto += cada_campo + '; '
    pets = conectar_mongo().pets
    resultado = pets.insert_one({
        'id_postgres': novo_pet.id,
        'nome': novo_pet.nome,
        'descricao': request.POST['descricao'],
        'ficha' : [],
        'ficha_texto': ficha_texto
        })
    for cada_campo in ficha:
        ChaveValor = cada_campo.split(":")
        pets.update({ '_id': resultado.inserted_id}, {'$push':{'ficha': {ChaveValor[0]: ChaveValor[1]}}})

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
