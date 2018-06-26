from django.shortcuts import render, redirect
from datetime import datetime

from processos_doacao.models import ProcessoDoacao
from anuncios_doacao.models import AnuncioDoacao


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
    processos = ProcessoDoacao.objects.filter(anuncio_id=anuncio_id)
    return render(request, 'processos_doacao/index.html', {'anuncio':anuncio, 'processos':processos})
