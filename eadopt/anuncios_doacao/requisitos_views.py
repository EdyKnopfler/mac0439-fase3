from django.shortcuts import render, redirect
from bson.objectid import ObjectId

from anuncios_doacao.models import AnuncioDoacao, Requisito
from eadopt.mongo import conectar_mongo
from autenticacao.autorizacao import *

def requisitos(request, anuncio_id):
    anuncio = AnuncioDoacao.objects.get(id=anuncio_id)
    requisitos = Requisito.objects.filter(anuncio_id=anuncio_id)
    return render(request, 'requisitos/index.html', {'anuncio':anuncio, 'requisitos':requisitos})


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
