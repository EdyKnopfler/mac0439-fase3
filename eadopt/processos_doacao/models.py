from django.db import models

from usuarios.models import Usuario
from anuncios_doacao.models import AnuncioDoacao

class ProcessoDoacao(models.Model):
    anuncio = models.ForeignKey(AnuncioDoacao, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_inicio = models.DateField(null=False)
    data_termino = models.DateField(null=False)
    
    class Meta:
        db_table = 'processo_doacao'
        unique_together = (('anuncio', 'candidato'),)

class StatusRequisito(models.Model):
    anuncio = models.ForeignKey(AnuncioDoacao, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=80, null=False, blank=False)
    status = models.CharField(max_length=12, null=False, blank=False, default='a verificar')
    
    class Meta:
        db_table = 'status_requisito'
        unique_together = (('anuncio', 'candidato', 'titulo'),)


