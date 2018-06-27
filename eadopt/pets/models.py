from django.db import models

from usuarios.models import Usuario

class Pet(models.Model):
    dono = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=80, null=False, blank=False)
    especie = models.CharField(max_length=80, null=False, blank=False)
    data_nascimento = models.DateField(null=True, blank=True)
    id_mongo = models.CharField(max_length=24, null=True, blank=True)

class Foto(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    arquivo = models.FileField(blank=False, default = 'placeholder.jpg')
