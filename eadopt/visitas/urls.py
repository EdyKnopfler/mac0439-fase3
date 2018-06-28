from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='visitas_index'),
    url(r'^criar/$', views.criar, name='visitas_criar'),
    url(r'^convidar/$', views.convidar, name='visitas_convidar'),
    #url(r'^remover/$', views.delete, name='usuario_remover')
]
