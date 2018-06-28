from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='visitas_index'),
    url(r'^criar/$', views.criar, name='visitas_criar'),
    url(r'^convidar/$', views.convidar, name='visitas_convidar'),
    url(r'^remover/(?P<visita_id>\d+)$', views.remover, name='visitas_remover')
]
