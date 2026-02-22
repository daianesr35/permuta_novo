from django.contrib import admin
from .models import Turma, Disciplina, HorarioAula


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("codigo_turma", "curso", "periodo", "turno", "usuario_admin", "data_cadastro")
    search_fields = ("codigo_turma", "curso", "periodo")
    list_filter = ("turno", "curso")
    ordering = ("curso", "codigo_turma")


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ("nome", "carga_horaria", "professor_responsavel", "usuario_admin", "data_cadastro")
    search_fields = ("nome", "professor_responsavel__user__first_name", "professor_responsavel__user__last_name")
    list_filter = ("professor_responsavel",)
    ordering = ("nome",)


@admin.register(HorarioAula)
class HorarioAulaAdmin(admin.ModelAdmin):
    list_display = (
        "turma",
        "disciplina",
        "professor",
        "dia_semana",
        "hora_inicio",
        "hora_fim",
        "usuario_admin",
        "data_cadastro",
    )
    list_filter = ("dia_semana", "turma", "professor")
    search_fields = (
        "turma__codigo_turma",
        "disciplina__nome",
        "professor__user__first_name",
        "professor__user__last_name",
    )
    ordering = ("turma", "dia_semana", "hora_inicio")
