from django.shortcuts import render, redirect
from datetime import datetime

from processos_doacao.models import ProcessoDoacao, StatusRequisito
from anuncios_doacao.models import AnuncioDoacao
from autenticacao.autorizacao import *


BLOQUEIO = erro_autorizacao('somente o dono do Anúncio de Doação tem acesso a esta funcionalidade')


def criar(request, anuncio_id):
    anuncio = AnuncioDoacao.objects.get(id=anuncio_id)
    novo_processo = ProcessoDoacao()
    novo_processo.anuncio_id = anuncio_id
    novo_processo.candidato_id = request.session['usuario_id']
    novo_processo.data_inicio = datetime.date(datetime.now())
    novo_processo.data_termino = anuncio.data_termino
    novo_processo.save()
    # status de requisitos são inseridos automaticamente via trigger para cada requisito do anúncio
    return redirect('anuncio_visualizar', anuncio_id)


def cancelar(request, anuncio_id):
    ProcessoDoacao.objects.get(anuncio_id=anuncio_id, candidato_id=request.session['usuario_id']).delete()
    return redirect('anuncio_visualizar', anuncio_id)
    
    
def candidatos(request, anuncio_id):
    anuncio = AnuncioDoacao.objects.get(id=anuncio_id)
    if not dono_anuncio(request, anuncio): return BLOQUEIO
    processos = ProcessoDoacao.objects.filter(anuncio_id=anuncio_id)
    return render(request, 'processos_doacao/index.html', {'anuncio':anuncio, 'processos':processos})
    
    
def requisitos(request, processo_id):
    processo = ProcessoDoacao.objects.get(id=processo_id)
    if not dono_anuncio(request, processo.anuncio): return BLOQUEIO
    status_req = StatusRequisito.objects.filter(anuncio_id=processo.anuncio_id, candidato_id=processo.candidato_id)
    return render(request, 'processos_doacao/requisitos.html', {'candidato':processo.candidato.nome, 
            'processo_id':processo_id, 'status_req':status_req})
    
    
def atualizar_requisitos(request):
    processo = ProcessoDoacao.objects.get(id=request.POST['processo_id'])
    if not dono_anuncio(request, processo.anuncio): return BLOQUEIO
    status_req = StatusRequisito.objects.filter(anuncio_id=processo.anuncio_id, candidato_id=processo.candidato_id)
    for s in status_req:
        s.status = request.POST['status[' + str(s.id) + ']']
        print(s.status)
        s.save()
    return redirect('processo_index', processo.anuncio_id)
    
