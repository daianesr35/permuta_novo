from django.contrib import admin
from django.utils import timezone
from .models import Permuta, Reposicao


@admin.register(Permuta)
class PermutaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "professor_solicitante",
        "professor_substituto",
        "status",
        "data_solicitacao",
        "data_decisao",
    )
    list_filter = ("status", "data_solicitacao")
    search_fields = (
        "id",
        "professor_solicitante__nome",
        "professor_substituto__nome",
        "horario__turma__codigo_turma",
        "horario__disciplina__nome",
    )

    # Campos apenas para visualização (não editar)
    readonly_fields = (
        "professor_solicitante",
        "professor_substituto",
        "horario",
        "data_solicitacao",
        "data_decisao",
        "usuario_decisor",
        "data_aula",
        "status",
    )

    def has_add_permission(self, request):
        # Não criar permutas pelo admin, apenas pelas telas do sistema
        return False

    def has_change_permission(self, request, obj=None):
        # Permite listar e abrir o detalhe, mas não salvar alterações
        base_perm = super().has_change_permission(request, obj)
        if not base_perm:
            return False
        if obj is None:
            # pode ver a lista
            return True
        # não pode alterar nenhum registro
        return False

    def has_delete_permission(self, request, obj=None):
        # proíbe excluir permutas via admin
        return False


@admin.register(Reposicao)
class ReposicaoAdmin(admin.ModelAdmin):
    list_display = ("id", "permuta", "data_reposicao")
    list_filter = ("data_reposicao",)
    search_fields = ("permuta__id",)

    readonly_fields = (
        "permuta",
        "data_reposicao",
        "observacao",
    )

    def has_add_permission(self, request):
        # Reposição sempre criada pelas telas do sistema, não pelo admin
        return False

    def has_change_permission(self, request, obj=None):
        base_perm = super().has_change_permission(request, obj)
        if not base_perm:
            return False
        if obj is None:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False