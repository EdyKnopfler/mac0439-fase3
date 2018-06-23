from django.http import HttpResponse

from pets.models import Pet
from anuncios_doacao.models import AnuncioDoacao

def erro_autorizacao(msg):
    return HttpResponse("ERRO DE AUTORIZAÇÃO: " + msg)

def dono_pet(request, campo):
    pet = Pet.objects.get(id=request.POST[campo])
    return pet.dono_id == request.session['usuario_id']

def dono_anuncio(request, anuncio):
    # olhamos o pet original do anúncio
    return anuncio.pet.dono_id == request.session['usuario_id']
    
def dono_anuncio2(request, campo):
    anuncio = AnuncioDoacao.objects.get(id=request.POST[campo])
    return anuncio.pet.dono_id == request.session['usuario_id']
