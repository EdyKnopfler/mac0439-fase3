from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^candidatar/(?P<anuncio_id>\d+)$', views.criar, name='processo_criar'),
    url(r'^cancelar/(?P<anuncio_id>\d+)$', views.cancelar, name='processo_cancelar'),
    url(r'^candidatos/(?P<anuncio_id>\d+)$', views.candidatos, name='processo_index'),
    url(r'^requisitos-candidato/(?P<processo_id>\d+)$', views.requisitos, name='processo_requisitos'),
    url(r'^atualizar-requisitos/$', views.atualizar_requisitos, name='processo_requisitos_atualizar'),
]
