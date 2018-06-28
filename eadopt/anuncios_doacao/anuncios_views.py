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


def index(request):
    meus_pets = Pet.objects.filter(dono_id=request.session['usuario_id'])
    meus_anuncios = AnuncioDoacao.objects.filter(pet__in=meus_pets).exclude(status='Finalizado')
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
        id_mongo = anuncio.id_mongo
        anuncio.delete()  # se der erro de integridade referencial, não excluir do MongoDB!!!
        conectar_mongo().anuncios.delete_one({"_id": ObjectId(id_mongo)})
    except ProtectedError:
        messages.warning(request, 'Ainda há candidatos!')
    return redirect('anuncio_index')
    
    
def busca(request):
    busca_dic = {"$text": {"$search": request.GET['q']}}
    mongo = conectar_mongo()
    
    busca_pets = mongo.pets.find(busca_dic)
    ids_pets = []
    for p in busca_pets:
        ids_pets.append(p['id_postgres'])
      
    busca_anuncios = mongo.anuncios.find(busca_dic)
    ids_anuncios = []
    for a in busca_anuncios:
        ids_anuncios.append(a['id_postgres'])
    
    busca_requisitos = mongo.requisitos.find(busca_dic)
    for r in busca_requisitos:
        ids_anuncios.append(r['id_anuncio_postgres'])
        
    anuncios = AnuncioDoacao.objects.filter(
            Q(pet_id__in=ids_pets) | Q(id__in=ids_anuncios), 
            data_termino__gte=datetime.date(datetime.now())).exclude(status='Finalizado')
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
        
        
def encerrar(request, processo_vencedor_id):
    vencedor = ProcessoDoacao.objects.get(id=processo_vencedor_id)
    anuncio = vencedor.anuncio
    if not dono_anuncio(request, anuncio):
        return erro_autorizacao('detectada tentativa de alterar o status de um Anúncio pertencente a outro usuário')
    agora = datetime.date(datetime.now())
    # status do anúncio
    anuncio.data_termino = agora
    anuncio.status = 'Finalizado'
    anuncio.escolhido_id = vencedor.candidato_id
    anuncio.save()
    # status dos processos
    processos = ProcessoDoacao.objects.filter(anuncio_id=anuncio.id)
    for p in processos:
        p.data_termino = agora
        p.save()
    # transferência da propriedade do Pet
    anuncio.pet.dono_id = vencedor.candidato_id
    anuncio.pet.save()
    return redirect('anuncio_index')
    
    
def preencher_anuncio(anuncio, request):
    agora = datetime.date(datetime.now())
    anuncio.data_inicio = request.POST['data_inicio'] if request.POST['data_inicio'] != '' else agora
    daqui_um_mes = agora + timedelta(days=30)
    anuncio.data_termino = request.POST['data_termino'] if request.POST['data_termino'] != '' else daqui_um_mes
    anuncio.pet_id = request.POST['pet_id']
    return anuncio



