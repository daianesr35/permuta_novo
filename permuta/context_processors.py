from .models import Notificacao

def notificacoes_nao_lidas(request):
    if request.user.is_authenticated:
        notificacoes = Notificacao.objects.filter(
            usuario=request.user,
            lida=False
        ).order_by("-data_criacao")
        return {"notificacoes_nao_lidas": notificacoes}
    return {}
