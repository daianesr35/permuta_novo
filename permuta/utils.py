from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

def enviar_email_notificacao(usuario, assunto, template, contexto):
    """
    Envia email de notificação para um usuário
    """
    if not usuario or not usuario.email:
        return False
    
    try:
        mensagem_html = render_to_string(template, contexto)
        
        send_mail(
            subject=assunto,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            html_message=mensagem_html,
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def notificar_nova_permuta(permuta, request):
    """
    Notifica sobre nova permuta solicitada
    """
    # Notificar professor substituto
    contexto = {
        'permuta': permuta,
        'tipo': 'nova_permuta',
        'nome_solicitante': permuta.professor_solicitante.nome,
        'request': request,
    }
    
    enviar_email_notificacao(
        usuario=permuta.professor_substituto.user,
        assunto=f'[Sistema de Permuta] Nova Permuta #{permuta.id}',
        template='emails/notificacao_permuta.html',
        contexto=contexto
    )
    
    # Notificar coordenadores
    coordenadores = User.objects.filter(is_staff=True)
    for coord in coordenadores:
        if coord.email and coord != permuta.professor_solicitante.user and coord != permuta.professor_substituto.user:
            contexto['nome_coordenador'] = coord.get_full_name() or coord.username
            enviar_email_notificacao(
                usuario=coord,
                assunto=f'[Sistema de Permuta] Nova Permuta #{permuta.id}',
                template='emails/notificacao_coordenador.html',
                contexto=contexto
            )

def notificar_confirmacao_permuta(permuta, request):
    """
    Notifica sobre confirmação de permuta
    """
    contexto = {
        'permuta': permuta,
        'nome_substituto': permuta.professor_substituto.nome,
        'request': request,
    }
    
    # Notificar solicitante
    enviar_email_notificacao(
        usuario=permuta.professor_solicitante.user,
        assunto=f'[Sistema de Permuta] Permuta #{permuta.id} Confirmada',
        template='emails/confirmacao_permuta.html',
        contexto=contexto
    )
    
    # Notificar coordenadores
    coordenadores = User.objects.filter(is_staff=True)
    for coord in coordenadores:
        if coord.email and coord != permuta.professor_solicitante.user and coord != permuta.professor_substituto.user:
            contexto['nome_coordenador'] = coord.get_full_name() or coord.username
            enviar_email_notificacao(
                usuario=coord,
                assunto=f'[Sistema de Permuta] Permuta #{permuta.id} Confirmada',
                template='emails/confirmacao_coordenador.html',
                contexto=contexto
            )

def notificar_cancelamento_permuta(permuta, request):
    """
    Notifica sobre cancelamento de permuta
    """
    contexto = {
        'permuta': permuta,
        'nome_solicitante': permuta.professor_solicitante.nome,
        'request': request,
    }
    
    # Notificar substituto
    enviar_email_notificacao(
        usuario=permuta.professor_substituto.user,
        assunto=f'[Sistema de Permuta] Permuta #{permuta.id} Cancelada',
        template='emails/cancelamento_permuta.html',
        contexto=contexto
    )
    
    # Notificar coordenadores
    coordenadores = User.objects.filter(is_staff=True)
    for coord in coordenadores:
        if coord.email and coord != permuta.professor_solicitante.user and coord != permuta.professor_substituto.user:
            contexto['nome_coordenador'] = coord.get_full_name() or coord.username
            enviar_email_notificacao(
                usuario=coord,
                assunto=f'[Sistema de Permuta] Permuta #{permuta.id} Cancelada',
                template='emails/cancelamento_coordenador.html',
                contexto=contexto
            )