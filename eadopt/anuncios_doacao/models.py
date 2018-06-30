from django.db import models
from datetime import date

from pets.models import Pet
from usuarios.models import Usuario

class AnuncioDoacao(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    data_inicio = models.DateField(null=False)
    data_termino = models.DateField(null=False)
    status = models.CharField(max_length=10, null=False, blank=False, default='Iniciado')
    escolhido = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    id_mongo = models.CharField(max_length=24, null=True, blank=True)
    
    def prazo_encerrado(self):
        return date.today() > self.data_termino
    
    class Meta:
       db_table = 'anuncio_doacao'

class Requisito(models.Model):
    anuncio = models.ForeignKey(AnuncioDoacao, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=80, null=False, blank=False)
    id_mongo = models.CharField(max_length=24, null=True, blank=True)
    tipo = models.CharField(max_length=11, null=False, blank=False, default='Obrigatório')
    peso = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'requisito'
        unique_together = (('anuncio', 'titulo'),)
    
    
"""
                ( id )
                anúncio
           >                 <
          /                   \
requisito                       processo
(id_anuncio, titulo)           (id_anuncio, candidato)
         \                    /
        (id_anuncio, titulo, candidato)    
                status req.
"""

