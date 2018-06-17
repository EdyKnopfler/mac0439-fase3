from django.contrib import messages
from django.shortcuts import redirect

def autenticacao_middleware(get_response):
    def middleware(request):
        if not (request.path == '/usuarios/login/' or request.path == '/usuarios/entrar/' or request.path == '/usuarios/novo/' or request.path == '/usuarios/criar/') and 'usuario_id' not in request.session:
            messages.warning(request, 'Por favor, faça login.')
            return redirect('/usuarios/login/')

        response = get_response(request)
        return response

    return middleware
