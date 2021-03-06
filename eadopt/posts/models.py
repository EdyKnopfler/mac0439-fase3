from django.db import models

from usuarios.models import Usuario

class Post(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=80, null=False, blank=False)
    id_mongo = models.CharField(max_length=24, null=True, blank=True)
    arquivo = models.FileField(blank=True)
    video = models.BooleanField(max_length=3, blank=True, default = False)
    class Meta:
       db_table = 'post'

class MarcadoNoPost(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    class Meta:
       db_table = 'marcado_no_post'
