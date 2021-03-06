from django.db import models

from usuarios.models import Usuario
from pets.models import Pet

class Visita(models.Model):
    visitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=False)
    comentario = models.CharField(max_length=200, null=False, blank=False)
    class Meta:
       db_table = 'visita'
