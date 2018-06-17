from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='usuario_login'),
    url(r'^entrar/$', views.entrar, name='usuario_entrar'),
    url(r'^logout/$', views.logout, name='usuario_logout'),
    url(r'^novo/$', views.novo, name='usuario_novo'),
    url(r'^criar/$', views.criar, name='usuario_criar'),
    url(r'^editar/$', views.editar, name='usuario_editar'),
    url(r'^atualizar/$', views.atualizar, name='usuario_atualizar'),
    #url(r'^remover/$', views.delete, name='usuario_remover')
]
