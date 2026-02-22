from django.db import models
from django.contrib.auth.models import User
from accounts.models import Professor
from cadastros.models import HorarioAula

from django.core.exceptions import ObjectDoesNotExist






class Permuta(models.Model):
    """
    Representa a solicitação de permuta de aula feita por um professor.
    Corresponde à entidade PERMUTA do MER/DER.
    """

    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("APROVADA", "Aprovada"),
        ("RECUSADA", "Recusada"),
        ("CANCELADA", "Cancelada"),
    ]
    
    status = models.CharField(
        max_length=10,  
        choices=STATUS_CHOICES,
        default="PENDENTE",
    )

    # Dados principais da permuta
    data_aula = models.DateField(
        verbose_name="Data da aula a ser permutada"
    )
    motivo = models.TextField(
        verbose_name="Motivo da permuta"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDENTE",
        verbose_name="Status da solicitação"
    )

    data_solicitacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data/hora da solicitação"
    )
    data_decisao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data/hora da decisão"
    )

    # Relacionamentos principais
    professor_solicitante = models.ForeignKey(
        Professor,
        on_delete=models.PROTECT,
        related_name="permutas_solicitadas",
        verbose_name="Professor solicitante"
    )
    professor_substituto = models.ForeignKey(
        Professor,
        on_delete=models.PROTECT,
        related_name="permutas_como_substituto",
        verbose_name="Professor substituto"
    )
    horario = models.ForeignKey(
        HorarioAula,
        on_delete=models.PROTECT,
        verbose_name="Horário de aula"
    )

    # Quem decidiu (coordenação/ADMIN)
    usuario_decisor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="permutas_decididas",
        verbose_name="Usuário que decidiu a permuta"
    )

    class Meta:
        verbose_name = "Permuta"
        verbose_name_plural = "Permutas"
        ordering = ["-data_solicitacao"]

    def __str__(self):
        return f"Permuta #{self.id} - {self.professor_solicitante.nome} → {self.professor_substituto.nome} em {self.data_aula}"
    
    def __str__(self):
        return f"Permuta #{self.id} - {self.professor_solicitante.nome} → {self.professor_substituto.nome} em {self.data_aula}"

    def tem_reposicao(self):
        """
        Retorna True se já existir uma reposição associada a esta permuta.
        """
        try:
            _ = self.reposicao
            return True
        except ObjectDoesNotExist:
            return False


class Reposicao(models.Model):
    """
    Representa a reposição de uma aula relacionada a uma permuta.
    Corresponde à entidade REPOSICAO do MER/DER.
    """

    permuta = models.OneToOneField(
        Permuta,
        on_delete=models.CASCADE,
        related_name="reposicao",
        verbose_name="Permuta relacionada"
    )
    data_reposicao = models.DateField(
        verbose_name="Data da reposição"
    )
    observacao = models.TextField(
        blank=True,
        verbose_name="Observações"
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de registro"
    )

    class Meta:
        verbose_name = "Reposição"
        verbose_name_plural = "Reposições"
        ordering = ["-data_reposicao"]

    def __str__(self):
        return f"Reposição da permuta #{self.permuta.id} em {self.data_reposicao}"
    
class Notificacao(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notificacoes"
    )
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    link = models.CharField(
        max_length=255,
        blank=True,
        help_text="URL interna para onde o usuário será redirecionado ao clicar na notificação."
    )

    class Meta:
        ordering = ["-data_criacao"]

    def __str__(self):
        estado = "Lida" if self.lida else "Não lida"
        return f"{self.usuario.username} - {self.mensagem[:40]}... ({estado})"

