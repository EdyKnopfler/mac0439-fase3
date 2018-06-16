from django.db import models

class Usuario(models.Model):
   email = models.CharField(max_length=80)
   senha = models.CharField(max_length=20)
   nome = models.CharField(max_length=80)

class PF(Usuario):
   cpf = models.CharField(max_length=11)
   
class PJ(Usuario):
   cnpj = models.CharField(max_length=14)
