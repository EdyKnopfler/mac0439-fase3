from django.db import models

from usuarios.models import Usuario

class Post(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=80, null=False, blank=False)
    id_mongo = models.CharField(max_length=24, null=True, blank=True)
    tem_midia = models.BooleanField()

class Midia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    binario = models.BinaryField(null=False, blank=False)
    formato = models.CharField(max_length=11, null=False, blank=False)

class MarcadoNoPost(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
