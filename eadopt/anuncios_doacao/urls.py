from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='anuncio_index'),
    url(r'^novo/$', views.novo, name='anuncio_novo'),
    url(r'^criar/$', views.criar, name='anuncio_criar'),
    url(r'^editar/(?P<anuncio_id>\d+)$', views.editar, name='anuncio_editar'),
    url(r'^excluir/(?P<anuncio_id>\d+)$', views.excluir, name='anuncio_excluir'),
    url(r'^atualizar/$', views.atualizar, name='anuncio_atualizar'),
    url(r'^busca/$', views.busca, name='anuncio_busca'),
    url(r'^visualizar/(?P<anuncio_id>\d+)$', views.visualizar, name='anuncio_visualizar'),
    url(r'^(?P<anuncio_id>\d+)/requisitos/$', views.requisitos, name='requisito_index'),
    url(r'^(?P<anuncio_id>\d+)/requisitos/novo$', views.novo_requisito, name='requisito_novo'),
    url(r'^requisitos/criar/$', views.criar_requisito, name='requisito_criar'),
    url(r'^requisitos/editar/(?P<requisito_id>\d+)$', views.editar_requisito, name='requisito_editar'),
    url(r'^requisitos/atualizar/$', views.atualizar_requisito, name='requisito_atualizar'),
    url(r'^requisitos/excluir/(?P<requisito_id>\d+)$', views.excluir_requisito, name='requisito_excluir'),
]
