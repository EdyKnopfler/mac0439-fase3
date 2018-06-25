from django.db import models

from usuarios.models import Usuario

class Post(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=80, null=False, blank=False)
    id_mongo = models.CharField(max_length=24, null=True, blank=True)
    arquivo = models.FileField(blank=True)

class MarcadoNoPost(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
