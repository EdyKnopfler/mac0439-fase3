from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='pets_index'),
    url(r'^novo/$', views.novo, name='pet_novo'),
    url(r'^criar/$', views.criar, name='pet_criar'),
    url(r'^perfil/(?P<pet_id>\d+)$', views.perfil, name='pet_perfil'),
    url(r'^editar/(?P<pet_id>\d+)$', views.editar, name='pet_editar'),
   	url(r'^atualizar/$', views.atualizar, name='pet_atualizar'),
    url(r'^remover/(?P<pet_id>\d+)$', views.remover, name='pet_remover')
]
