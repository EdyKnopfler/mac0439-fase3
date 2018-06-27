from django.conf.urls import url

from . import anuncios_views, requisitos_views

urlpatterns = [
    url(r'^$', anuncios_views.index, name='anuncio_index'),
    url(r'^novo/$', anuncios_views.novo, name='anuncio_novo'),
    url(r'^criar/$', anuncios_views.criar, name='anuncio_criar'),
    url(r'^editar/(?P<anuncio_id>\d+)$', anuncios_views.editar, name='anuncio_editar'),
    url(r'^excluir/(?P<anuncio_id>\d+)$', anuncios_views.excluir, name='anuncio_excluir'),
    url(r'^atualizar/$', anuncios_views.atualizar, name='anuncio_atualizar'),
    url(r'^busca/$', anuncios_views.busca, name='anuncio_busca'),
    url(r'^visualizar/(?P<anuncio_id>\d+)$', anuncios_views.visualizar, name='anuncio_visualizar'),
    
    url(r'^(?P<anuncio_id>\d+)/requisitos/$', requisitos_views.requisitos, name='requisito_index'),
    url(r'^(?P<anuncio_id>\d+)/requisitos/novo$', requisitos_views.novo_requisito, name='requisito_novo'),
    url(r'^requisitos/criar/$', requisitos_views.criar_requisito, name='requisito_criar'),
    url(r'^requisitos/editar/(?P<requisito_id>\d+)$', requisitos_views.editar_requisito, name='requisito_editar'),
    url(r'^requisitos/atualizar/$', requisitos_views.atualizar_requisito, name='requisito_atualizar'),
    url(r'^requisitos/excluir/(?P<requisito_id>\d+)$', requisitos_views.excluir_requisito, name='requisito_excluir'),
]
