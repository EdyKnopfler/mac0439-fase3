from usuarios.models import Usuario
from posts.models import Post
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
from datetime import datetime
import sys

def perfil(request):
    return perfilOutros (request, request.session["usuario_id"] )

def perfilOutros(request, user_id):
    if user_id == request.session["usuario_id"] or user_id == '':
        user_id = request.session["usuario_id"]
        owner = True
    else:
        owner = False

    usuario = Usuario.objects.get(id=user_id)

    doc = conectar_mongo().usuarios.find_one({"_id": ObjectId(usuario.id_mongo)})
    # return render(request, 'editar.html', {"usuario":usuario, "descricao": doc['descricao']})

    try:
        posts = Post.objects.filter(usuario_id=user_id).order_by('-data_hora')[0:5]
        for post in posts:
            post.texto = conectar_mongo().posts.find_one({"id_postgres" : post.id})['texto']
    except:
        e = sys.exc_info()
        print("erro!")
        print(e)
        posts = []

    return render(request, 'perfil.html', {"usuario":usuario, "descricao": doc['descricao'], "posts":posts, "editavel":owner})

def posts(request):
    return postsOutros(request, request.session["usuario_id"])

def postsOutros(request, user_id):
    if user_id == request.session["usuario_id"] or user_id == '':
        user_id = request.session["usuario_id"]
        owner = True
    else:
        owner = False
    try:
        posts = Post.objects.filter(usuario_id=user_id).order_by('-data_hora')
        for post in posts:
            post.texto = conectar_mongo().posts.find_one({"id_postgres" : post.id})['texto']
    except:
        e = sys.exc_info()
        print("erro!")
        print(e)
        posts = []

    return render(request, 'lista_posts.html', {"posts":posts, "editavel":owner})

def novo(request):
    return render(request, 'novo_post.html')

def preencher(request):
    post = Post()
    post.titulo = request.POST['titulo']
    post.data_hora = datetime.date(datetime.now())
    post.tem_midia = False
    post.usuario_id = request.session['usuario_id']
    return post

def criar(request):
    novo_post = preencher(request)
    novo_post.save()
    resultado = conectar_mongo().posts.insert_one({
        'id_postgres': novo_post.id,
        #'id_usuario': request.session["usuario_id"],
        'texto': request.POST['texto']
        })
    novo_post.id_mongo = str(resultado.inserted_id)
    novo_post.save()
    return redirect('perfil')

def editar (request):
    return redirect('perfil')

def editarId(request, post_id):
    post = Post.objects.get(id=post_id)

    if post.usuario_id != request.session['usuario_id']:
        return erro_autorizacao('Você não tem permissão para editar este post!')

    post.texto = conectar_mongo().posts.find_one({"id_postgres" : post.id})['texto']
    return render(request, 'editar_post.html', {'post':post})

def atualizar(request):
    existente = Post.objects.get(id=request.POST['post_id'])
    existente.titulo = request.POST['titulo']
    existente.save()
    conectar_mongo().posts.update_one({"_id": ObjectId(existente.id_mongo)}, {
        "$set": {'texto':request.POST['texto']}
    })
    return redirect('perfil')
