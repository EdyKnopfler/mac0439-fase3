from django.shortcuts import render
from usuarios.models import Usuario, PF, PJ
from posts.models import Post
from django.contrib import messages
from django.shortcuts import render, redirect
from eadopt.mongo import conectar_mongo
from bson.objectid import ObjectId
import django.utils.formats as fmt

def login(request):
    return render(request, 'login.html')


def entrar(request):
    mensagem = 'E-mail ou senha inválidos. Verifique os dados e tente novamente.'
    try:
        usuario_existente = Usuario.objects.get(email=request.POST['email'])
        if usuario_existente.email == request.POST['email'] and usuario_existente.senha == request.POST['senha']:
            set_session(request, usuario_existente)
            return redirect('index')
        else:
            messages.warning(request, mensagem)
    except Usuario.DoesNotExist:
        messages.warning(request, mensagem)
    return redirect('usuario_login')


def index(request):
    if (request.session['tipo'] == "pf"):
        usuario = PF.objects.get(id=request.session["usuario_id"])
    else:
        usuario = PJ.objects.get(id=request.session["usuario_id"])

    doc = conectar_mongo().usuarios.find_one({"_id": ObjectId(request.session['usuario_mongo_id'])})

    if doc:
        descricao = doc['descricao']
    else:
        descricao = ''

    posts = Post.objects.all().order_by('-data_hora')[0:20]
    for post in posts:
        try:
            post.autor = Usuario.objects.get(id=post.usuario_id).nome
        except Exception:
            post.autor = Usuario.objects.get(id=post.usuario_id).email
    # return render(request, 'editar.html', {"usuario":usuario, "descricao": doc['descricao']})
    return render(request, 'index.html', {"usuario":usuario, "descricao": descricao, "posts":posts})


def logout(request):
    request.session.flush()
    return redirect('usuario_login')


def novo(request):
    return render(request, 'novo.html')


def criar(request):
    novo_usuario = preencher(request)
    novo_usuario.save()
    db = conectar_mongo()
    sitedb = db.usuarios
    resultado = sitedb.insert_one({
        'id_postgres': novo_usuario.id,
        'nome': novo_usuario.nome,
        'descricao': request.POST['descricao']
        })
    novo_usuario.id_mongo = str(resultado.inserted_id)
    novo_usuario.save()
    set_session(request, novo_usuario)
    return redirect('index')


def editar(request):
    if (request.session['tipo'] == "pf"):
        usuario = PF.objects.get(id=request.session["usuario_id"])
    else:
        usuario = PJ.objects.get(id=request.session["usuario_id"])

    doc = conectar_mongo().usuarios.find_one({"_id": ObjectId(request.session['usuario_mongo_id'])})
    return render(request, 'editar.html', {"usuario":usuario, "descricao": doc['descricao']})


def atualizar(request):
    usuario_editado = preencher(request)
    usuario_editado.id = request.session['usuario_id']
    usuario_editado.save()
    conectar_mongo().usuarios.update_one({"_id": ObjectId(request.session['usuario_mongo_id'])}, {
        "$set": {'nome':request.POST['nome'], 'descricao': request.POST['descricao']}
    })
    return redirect('index')


def set_session(request, usuario):
    request.session['usuario_id'] = usuario.id
    request.session['usuario_mongo_id'] = usuario.id_mongo
    request.session['tipo'] = usuario.tipo


def preencher(request):
    if 'tipo' in request.session:
        tipo = request.session['tipo']
    else:
        tipo = request.POST['tipo']

    if tipo == 'pf':
        usuario = PF()
        usuario.cpf = request.POST['cpf']
        if request.POST['data_nascimento'] != '':
            usuario.data_nascimento = request.POST['data_nascimento']
        else:
            usuario.data_nascimento = None
    else:
        usuario = PJ()
        usuario.cnpj = request.POST['cnpj']

    usuario.tipo = tipo
    usuario.nome = request.POST['nome']
    usuario.email = request.POST['email']
    usuario.senha = request.POST['senha']
    usuario.rua = request.POST['rua']
    usuario.bairro = request.POST['bairro']
    usuario.cidade = request.POST['cidade']
    usuario.estado = request.POST['estado']
    usuario.cep = request.POST['cep']
    usuario.telefone = request.POST['telefone']

    try:
        latitude = float(request.POST['latitude'].replace(fmt.get_format("DECIMAL_SEPARATOR"), '.'))
    except:
        latitude = 0

    try:
        longitude = float(request.POST['longitude'].replace(fmt.get_format("DECIMAL_SEPARATOR"), '.'))
    except:
        longitude = 0

    usuario.latitude = latitude
    usuario.longitude = longitude

    return usuario
