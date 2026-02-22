"""
URL Configuration for permuta_aulas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from permuta.views import (
    # Páginas principais
    home,
    meu_logout,
    
    # Dashboards
    professor_dashboard,
    admin_dashboard,
    
    # Professor - Horários
    meus_horarios,
    solicitar_permuta,
    calendario_horarios,
    api_eventos_calendario,
    
    # Professor - Permutas
    minhas_permutas,
    detalhe_permuta,
    cancelar_permuta,
    comprovante_permuta_pdf,
    
    # Professor - Reposições
    registrar_reposicao,
    
    # Professor - Como substituto
    permutas_como_substituto,
    confirmar_permuta_substituto,
    
    # Coordenação
    permutas_pendentes,
    dashboard_estatisticas,
    relatorio_permutas_excel,
    relatorio_permutas_pdf,
    
    # API
    api_permutas,
    api_permuta_detalhe,
    api_estatisticas,
    api_notificacoes_nao_lidas,
    
    # Notificações
    ler_notificacao,
)


urlpatterns = [
    # PÁGINA INICIAL (deve vir antes de tudo)
    # -----------------------------------------------------------------
    path("", home, name="home"),

    # AUTENTICAÇÃO
    # -----------------------------------------------------------------
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", meu_logout, name="logout"),

    # ========================================================================
    # DASHBOARDS - COLOCADOS ANTES DO ADMIN PARA EVITAR CONFLITO!
    # ========================================================================
    path(
        "admin/dashboard/",
        admin_dashboard,
        name="admin_dashboard",
    ),
    path(
        "professor/dashboard/",
        professor_dashboard,
        name="professor_dashboard",
    ),

    # ========================================================================
    # PROFESSOR - HORÁRIOS
    # ========================================================================
    path(
        "professor/horarios/",
        meus_horarios,
        name="meus_horarios",
    ),
    path(
        "professor/calendario/",
        calendario_horarios,
        name="calendario_horarios",
    ),
    path(
        "api/eventos-calendario/",
        api_eventos_calendario,
        name="api_eventos_calendario",
    ),
    path(
        "professor/horarios/<int:horario_id>/solicitar-permuta/",
        solicitar_permuta,
        name="solicitar_permuta",
    ),

    # ========================================================================
    # PROFESSOR - PERMUTAS
    # ========================================================================
    path(
        "professor/permutas/",
        minhas_permutas,
        name="minhas_permutas",
    ),
    path(
        "professor/permutas/<int:permuta_id>/",
        detalhe_permuta,
        name="detalhe_permuta",
    ),
    path(
        "professor/permutas/<int:permuta_id>/cancelar/",
        cancelar_permuta,
        name="cancelar_permuta",
    ),
    path(
        "professor/permutas/<int:permuta_id>/comprovante-pdf/",
        comprovante_permuta_pdf,
        name="comprovante_permuta_pdf",
    ),

    # ========================================================================
    # PROFESSOR - REPOSIÇÕES
    # ========================================================================
    path(
        "professor/permutas/<int:permuta_id>/registrar-reposicao/",
        registrar_reposicao,
        name="registrar_reposicao",
    ),

    # ========================================================================
    # PROFESSOR - COMO SUBSTITUTO
    # ========================================================================
    path(
        "professor/permutas/como-substituto/",
        permutas_como_substituto,
        name="permutas_como_substituto",
    ),
    path(
        "professor/permutas/<int:permuta_id>/confirmar/",
        confirmar_permuta_substituto,
        name="confirmar_permuta_substituto",
    ),

    # ========================================================================
    # COORDENAÇÃO / ADMIN
    # ========================================================================
    path(
        "coordenacao/permutas/pendentes/",
        permutas_pendentes,
        name="permutas_pendentes",
    ),
    path(
        "coordenacao/dashboard/estatisticas/",
        dashboard_estatisticas,
        name="dashboard_estatisticas",
    ),
    path(
        "coordenacao/relatorios/excel/",
        relatorio_permutas_excel,
        name="relatorio_permutas_excel",
    ),
    path(
        "coordenacao/relatorios/pdf/",
        relatorio_permutas_pdf,
        name="relatorio_permutas_pdf",
    ),

    # ========================================================================
    # API
    # ========================================================================
    path(
        "api/permutas/",
        api_permutas,
        name="api_permutas",
    ),
    path(
        "api/permutas/<int:permuta_id>/",
        api_permuta_detalhe,
        name="api_permuta_detalhe",
    ),
    path(
        "api/estatisticas/",
        api_estatisticas,
        name="api_estatisticas",
    ),
    path(
        "api/notificacoes/",
        api_notificacoes_nao_lidas,
        name="api_notificacoes",
    ),

    # ========================================================================
    # NOTIFICAÇÕES
    # ========================================================================
    path(
        "notificacoes/<int:notificacao_id>/ler/",
        ler_notificacao,
        name="ler_notificacao",
    ),

    # ========================================================================
    # ADMIN DO DJANGO - DEVE VIR POR ÚLTIMO!
    # ========================================================================
    path("admin/", admin.site.urls, name="admin"),
]