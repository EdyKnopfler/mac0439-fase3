from usuarios.models import Usuario
from django.db.models import Q
from posts.models import Post, MarcadoNoPost
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import sys
import os
import json

def get_user_names(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        nomes = Usuario.objects.filter(Q(nome__icontains = q) | Q(email__icontains = q) )[:10]
        results = []
        for n in nomes:
            info = {}
            info['label'] = n.nome + " (" + n.email + ")"
            info['id'] = n.id
            results.append(info)
        data = json.dumps(results)
    else:
        data = 'fail'
    # print(data)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def perfil(request):
    return perfilOutros (request, request.session["usuario_id"] )

class Tageados(object):
    def __init__(self, nome, id):
        self.nome = nome
        self.id = id

def perfilOutros(request, user_id):
    if int(user_id) == int(request.session["usuario_id"]) or user_id == '':
        user_id = request.session["usuario_id"]
        owner = True
    else:
        owner = False

    usuario = Usuario.objects.get(id=user_id)

    doc = conectar_mongo().usuarios.find_one({"_id": ObjectId(usuario.id_mongo)})

    if doc:
        descricao = doc['descricao']
    else:
        descricao = ''

    try:
        posts = Post.objects.filter(usuario_id=user_id).order_by('-data_hora')[0:5]
        for post in posts:
            texto_mongo = conectar_mongo().posts.find_one({"id_postgres" : post.id})
            if texto_mongo:
                post.texto = texto_mongo['texto']
    except Exception:
        posts = []

    for post in posts:
        marcados = MarcadoNoPost.objects.filter(post_id = post.id)
        post.marcados = []
        for marcado in marcados:
            pessoa = Usuario.objects.get(id=marcado.usuario_id)
            aux = Tageados(pessoa.nome, pessoa.id)
            post.marcados += [aux]

    return render(request, 'perfil.html', {"usuario":usuario, "descricao":descricao, "posts":posts, "editavel":owner})

def posts(request):
    return postsOutros(request, request.session["usuario_id"])

def postsOutros(request, user_id):
    if int(user_id) == int(request.session["usuario_id"]) or user_id == '':
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

def criar(request):
    # print(request.POST)
    novo_post = preencher(request)
    novo_post.save()
    resultado = conectar_mongo().posts.insert_one({
        'id_postgres': novo_post.id,
        #'id_usuario': request.session["usuario_id"],
        'texto': request.POST['texto']
        })
    novo_post.id_mongo = str(resultado.inserted_id)
    novo_post.save()
    marcados = set(request.POST.getlist('marcados'))
    for marcado in marcados:
        email = marcado.split('(')[1]
        email = email[:len(email)-1]
        usuario = Usuario.objects.get(email=email)
        marcadoNoPost = MarcadoNoPost()
        marcadoNoPost.usuario_id = usuario.id
        post = Post.objects.get(id_mongo=novo_post.id_mongo)
        marcadoNoPost.post_id = post.id
        marcadoNoPost.save()

    return redirect('perfil')

def preencher(request):
    post = Post()
    try:
        # print(request.FILES)
        myFile = request.FILES['arquivo']
        fs = FileSystemStorage()
        filename, file_extension = os.path.splitext(myFile.name)
        filename = fs.save(
            str(request.session['usuario_id']) + file_extension, myFile)
        if (request.POST['fileType'] == 'vid'):
            post.video = True
    except Exception:
        filename = ''
    post.arquivo = filename
    post.titulo = request.POST['titulo']
    post.usuario_id = request.session['usuario_id']
    return post

def editar (request):
    return redirect('perfil')

def editarId(request, post_id):
    post = Post.objects.get(id=post_id)

    if post.usuario_id != request.session['usuario_id']:
        return erro_autorizacao('Você não tem permissão para editar este post!')

    post.texto = conectar_mongo().posts.find_one({"id_postgres" : post.id})['texto']

    marcados = MarcadoNoPost.objects.filter(post_id = post.id)
    post.marcados = []
    for marcado in marcados:
        pessoa = Usuario.objects.get(id=marcado.usuario_id)
        aux = Tageados(pessoa.nome + " (" + pessoa.email + ")", pessoa.id)
        post.marcados += [aux]

        #print(post.marcados)

    return render(request, 'editar_post.html', {'post':post})

def atualizar(request):
    # print(request.POST)
    existente = Post.objects.get(id=request.POST['post_id'])
    existente.titulo = request.POST['titulo']
    conectar_mongo().posts.update_one({"_id": ObjectId(existente.id_mongo)}, {
        "$set": {'texto':request.POST['texto']}
    })
    try:
        myFile = request.FILES['arquivo']
        fs = FileSystemStorage()
        filename, file_extension = os.path.splitext(myFile.name)
        filename = fs.save(
            str(request.session['usuario_id']) + file_extension, myFile)
        fs.delete(existente.arquivo)
        existente.arquivo = filename
        if (request.POST['fileType'] == 'vid'):
            existente.video = True
    except Exception:
        pass
    existente.save()

    marcados = request.POST.getlist('marcados')
    MarcadoNoPost.objects.filter(post_id = existente.id).delete()
    for marcado in marcados:
        email = marcado.split('(')[1]
        email = email[:len(email)-1]
        # print(email)
        usuario = Usuario.objects.get(email=email)
        marcadoNoPost = MarcadoNoPost()
        marcadoNoPost.usuario_id = usuario.id
        marcadoNoPost.post_id = existente.id
        marcadoNoPost.save()

    return redirect('perfil')
