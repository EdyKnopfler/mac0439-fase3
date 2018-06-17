from django.shortcuts import render
from usuarios.models import Usuario, PF, PJ
from django.contrib import messages
from django.shortcuts import render, redirect

def login(request):
    return render(request, 'login.html')
   
   
def entrar(request):
    mensagem = 'E-mail ou senha inválidos. Verifique os dados e tente novamente.'
    try:
        usuario_existente = Usuario.objects.get(email=request.POST['email'])
        if usuario_existente.email == request.POST['email'] and usuario_existente.senha == request.POST['senha']:
            request.session['usuario_id'] = usuario_existente.id
            return redirect('index')
        else:
            messages.warning(request, mensagem)
    except Usuario.DoesNotExist:
        messages.warning(request, mensagem)
    return redirect('usuario_login')
    
    
def index(request):
    return render(request, 'index.html')
    
    
def logout(request):
    request.session.flush()
    return redirect('usuario_login')
    
    
def novo(request):
    return render(request, 'novo.html')


def criar(request):
    if request.POST['tipo'] == 'pf':
        novo_usuario = PF()
        novo_usuario.cpf = request.POST['cpf']
        novo_usuario.data_nascimento = request.POST['data_nascimento']
    else:
        novo_usuario = PJ()
        novo_usuario.cnpj = request.POST['cnpj']
    
    novo_usuario.nome = request.POST['nome']
    novo_usuario.email = request.POST['email']
    novo_usuario.senha = request.POST['senha']
    novo_usuario.rua = request.POST['rua']
    novo_usuario.bairro = request.POST['bairro']
    novo_usuario.cidade = request.POST['cidade']
    novo_usuario.estado = request.POST['estado']
    novo_usuario.cep = request.POST['cep']
    novo_usuario.telefone = request.POST['telefone']
    novo_usuario.latitude = request.POST['latitude']
    novo_usuario.longitude = request.POST['longitude']

    novo_usuario.save()
    request.session['usuario_id'] = novo_usuario.id
    return redirect('index')
