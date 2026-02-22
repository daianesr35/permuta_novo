from django.contrib import admin
from .models import Professor


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "matricula_siape",
        "cpf",
        "coordenacao",
        "telefone",
        "usuario_admin",
        "data_cadastro",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "matricula_siape",
        "cpf",
    )
    list_filter = ("coordenacao", "usuario_admin")
    ordering = ("user__first_name", "user__last_name")
