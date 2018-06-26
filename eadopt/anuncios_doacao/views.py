from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from django.db.models import Q, ProtectedError

from pets.models import Pet
from anuncios_doacao.models import AnuncioDoacao, Requisito
from eadopt.mongo import conectar_mongo
from autenticacao.autorizacao import *
from processos_doacao.models import ProcessoDoacao, StatusRequisito


# TODO refatorar esta coisa que já está ficando enorme :P
# tentar quebrar o arquivo em dois e linká-nos no urls.py


def index(request):
    meus_pets = Pet.objects.filter(dono_id=request.session['usuario_id'])
    meus_anuncios = AnuncioDoacao.objects.filter(pet__in=meus_pets)
    meus_processos = ProcessoDoacao.objects.filter(candidato_id=request.session['usuario_id'])
    return render(request, 'anuncios/index.html', {'meus_anuncios':meus_anuncios, 'meus_processos':meus_processos})

    
def novo(request):
    pets = Pet.objects.filter(dono_id=request.session['usuario_id'])
    return render(request, 'anuncios/novo.html', {'pets':pets})
    
    
def criar(request):
    if not dono_pet(request, 'pet_id'):
        return erro_autorizacao('detectada possível manipulação do ID do Pet')
    novo_anuncio = preencher_anuncio(AnuncioDoacao(), request)
    novo_anuncio.save()
    resultado = conectar_mongo().anuncios.insert_one({
        'id_postgres': novo_anuncio.id,
        'descricao': request.POST['descricao']
    })
    novo_anuncio.id_mongo = str(resultado.inserted_id)
    novo_anuncio.save()
    return redirect('requisito_index', novo_anuncio.id)
    
    
def editar(request, anuncio_id):
    pets = Pet.objects.filter(dono_id=request.session['usuario_id'])
    anuncio = AnuncioDoacao.objects.get(id=anuncio_id)
    doc = conectar_mongo().anuncios.find_one({"_id": ObjectId(anuncio.id_mongo)})
    return render(request, 'anuncios/editar.html', {'pets': pets, 'anuncio':anuncio, 'descricao':doc['descricao']})


def atualizar(request):
    if not dono_pet(request, 'pet_id'):
        return erro_autorizacao('detectada possível manipulação do ID do Pet')
    existente = AnuncioDoacao.objects.get(id=request.POST['anuncio_id'])
    if not dono_anuncio(request, existente):
        return erro_autorizacao('detectada possível manipulação do ID do Anúncio de Doação')
    anuncio = preencher_anuncio(existente, request)
    anuncio.save()
    conectar_mongo().anuncios.update_one({"_id": ObjectId(anuncio.id_mongo)}, {
        "$set": {'descricao':request.POST['descricao']}
    })
    return redirect('anuncio_index')


def excluir(request, anuncio_id):
    try:
        anuncio = AnuncioDoacao.objects.get(id=anuncio_id)
        if not dono_anuncio(request, anuncio):
            return erro_autorizacao('detectada possível manipulação do ID do Anúncio de Doação')
        conectar_mongo().anuncios.delete_one({"_id": ObjectId(anuncio.id_mongo)})
        anuncio.delete()
    except ProtectedError:
        messages.warning(request, 'Ainda há candidatos!')
    return redirect('anuncio_index')
    
    
def busca(request):
    busca_dic = {"$text": {"$search": request.GET['q']}}
    mongo = conectar_mongo()
    
    busca_pets = mongo.pets.find(busca_dic)
    ids_pets = []
    for p in busca_pets:
        print("achei pet")
        ids_pets.append(p['id_postgres'])
      
    busca_anuncios = mongo.anuncios.find(busca_dic)
    ids_anuncios = []
    for a in busca_anuncios:
        print("achei anuncio")
        ids_anuncios.append(a['id_postgres'])
    
    busca_requisitos = mongo.requisitos.find(busca_dic)
    for r in busca_requisitos:
        print("achei requisito")
        ids_anuncios.append(r['id_anuncio_postgres'])
        
    anuncios = AnuncioDoacao.objects.filter(Q(pet_id__in=ids_pets) | Q(id__in=ids_anuncios))
    return render(request, 'anuncios/resultados_busca.html', {'anuncios':anuncios})
    
    
def visualizar(request, anuncio_id):
    anuncio = AnuncioDoacao.objects.get(id=anuncio_id)
    mongo = conectar_mongo()
    doc = mongo.anuncios.find_one({"_id": ObjectId(anuncio.id_mongo)})
    requisitos = Requisito.objects.filter(anuncio_id=anuncio_id)
    reqs_mongo = mongo.requisitos.find({'id_anuncio_postgres':anuncio_id})
    descricoes_reqs = {}
    for r in reqs_mongo:
        descricoes_reqs[r['id_postgres']] = r['descricao']
    status_requisitos = StatusRequisito.objects.filter(anuncio_id=anuncio_id,candidato_id=request.session['usuario_id'])
    status = {}
    for s in status_requisitos:
        status[s.titulo] = s.status
    return render(request, 'anuncios/visualizar.html', {'anuncio':anuncio, 'descricao':doc['descricao'], 
        'requisitos':requisitos, 'descricoes_reqs':descricoes_reqs, 'status':status})
    
    
def preencher_anuncio(anuncio, request):
    agora = datetime.date(datetime.now())
    anuncio.data_inicio = request.POST['data_inicio'] if request.POST['data_inicio'] != '' else agora
    daqui_um_mes = agora + timedelta(days=30)
    anuncio.data_termino = request.POST['data_termino'] if request.POST['data_termino'] != '' else daqui_um_mes
    anuncio.pet_id = request.POST['pet_id']
    return anuncio


def requisitos(request, anuncio_id):
    requisitos = Requisito.objects.filter(anuncio_id=anuncio_id)
    return render(request, 'requisitos/index.html', {'anuncio_id':anuncio_id, 'requisitos':requisitos})


def novo_requisito(request, anuncio_id):
    return render(request, 'requisitos/novo.html', {'anuncio_id': anuncio_id})
    
    
def criar_requisito(request):
    if not dono_anuncio2(request, 'anuncio_id'):
        return erro_autorizacao('detectada possível manipulação do ID do Anúncio de Doação')
    novo_req = preencher_requisito(Requisito(), request)
    novo_req.anuncio_id = request.POST['anuncio_id']
    novo_req.save()
    resultado = conectar_mongo().requisitos.insert_one({
        'id_postgres': novo_req.id,
        'id_anuncio_postgres': novo_req.anuncio_id,
        'titulo': request.POST['titulo'],
        'descricao': request.POST['descricao']
    })
    novo_req.id_mongo = str(resultado.inserted_id)
    novo_req.save()
    # status de requisito para todos os processos são inseridos automaticamente via trigger
    return redirect('requisito_index', novo_req.anuncio_id)


def editar_requisito(request, requisito_id):
    requisito = Requisito.objects.get(id=requisito_id)
    doc = conectar_mongo().requisitos.find_one({"_id": ObjectId(requisito.id_mongo)})
    return render(request, 'requisitos/editar.html', {
        'anuncio_id': requisito.anuncio_id, 'requisito':requisito, 'descricao':doc['descricao']})
    
    
def atualizar_requisito(request):
    requisito = Requisito.objects.get(id=request.POST['requisito_id'])
    if not dono_anuncio(request, requisito.anuncio):
        return erro_autorizacao('detectada possível manipulação do ID do Requisito')
    requisito = preencher_requisito(requisito, request)
    requisito.save()
    conectar_mongo().requisitos.update_one({"_id": ObjectId(requisito.id_mongo)}, {
        "$set": {'titulo':request.POST['titulo'], 'descricao':request.POST['descricao']}
    })
    return redirect('requisito_index', requisito.anuncio_id)
    
    
def excluir_requisito(request, requisito_id):
    requisito = Requisito.objects.get(id=requisito_id)
    if not dono_anuncio(request, requisito.anuncio):
        return erro_autorizacao('detectada possível manipulação do ID do Requisito')
    anuncio_id = requisito.anuncio_id
    conectar_mongo().requisitos.delete_one({"_id": ObjectId(requisito.id_mongo)})
    requisito.delete()
    return redirect('requisito_index', anuncio_id)


def preencher_requisito(requisito, request):
    requisito.titulo = request.POST['titulo']
    requisito.tipo = request.POST['tipo']
    if request.POST['tipo'] == 'Obrigatório':
        requisito.peso = None
    else:
        try:
            requisito.peso = int(request.POST['peso'])
        except:
            requisito.peso = 1
    return requisito
