from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.perfil, name='perfil'),
    url(r'^([0-9]+)/$', views.perfilOutros, name='perfil_outros'),
    url(r'^postar/$', views.novo, name='post_novo'),
    url(r'^criar/$', views.criar, name='post_criar'),
    url(r'^editar/$', views.editar, name='post_editar'),
    url(r'^editar/([0-9]+)/$', views.editarId, name='post_editar_id'),
    url(r'^atualizar/$', views.atualizar, name='post_atualizar'),
    url(r'^posts/$', views.posts, name='meus_posts'),
    url(r'^posts/([0-9]+)/$', views.postsOutros, name='post_outros'),
    url(r'^get_user_names/', views.get_user_names),
]
