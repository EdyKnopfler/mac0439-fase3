from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='anuncio_index'),
    url(r'^novo/$', views.novo, name='anuncio_novo'),
    url(r'^criar/$', views.criar, name='anuncio_criar'),
    url(r'^editar/(?P<anuncio_id>\d+)$', views.editar, name='anuncio_editar'),
    #url(r'^atualizar/$', views.atualizar, name='anuncio_atualizar'),
]
