from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^candidatar/(?P<anuncio_id>\d+)$', views.criar, name='processo_criar'),
    url(r'^cancelar/(?P<anuncio_id>\d+)$', views.cancelar, name='processo_cancelar'),
]
