from django.db import models

class Usuario(models.Model):
   email = models.CharField(max_length=80, null=False, blank=False, unique=True)
   senha = models.CharField(max_length=20, null=False, blank=False)
   nome = models.CharField(max_length=80, null=False, blank=False)
   rua = models.CharField(max_length=80, null=True, blank=True)
   bairro = models.CharField(max_length=80, null=True, blank=True)
   cidade = models.CharField(max_length=80, null=True, blank=True)
   estado = models.CharField(max_length=2, null=True, blank=True)
   cep = models.CharField(max_length=8, null=True, blank=True)
   telefone = models.CharField(max_length=11, null=True, blank=True)
   latitude = models.FloatField(null=True, blank=True)
   longitude = models.FloatField(null=True, blank=True)
   id_mongo = models.CharField(max_length=24, null=True, blank=True)

class PF(Usuario):
   cpf = models.CharField(max_length=11, unique=True)
   data_nascimento = models.DateField(null=True, blank=True)
   
class PJ(Usuario):
   cnpj = models.CharField(max_length=14, unique=True)
