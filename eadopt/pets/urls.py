from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='pets_index'),
    url(r'^novo/$', views.novo, name='pet_novo'),
    url(r'^criar/$', views.criar, name='pet_criar'),
    # url(r'^editar/$', views.editar, name='usuario_editar'),
    # url(r'^atualizar/$', views.atualizar, name='usuario_atualizar'),
    #url(r'^remover/$', views.delete, name='usuario_remover')
]
