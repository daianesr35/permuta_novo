from django.db import models
from django.contrib.auth.models import User
from accounts.models import Professor


class Turma(models.Model):
    """
    Representa uma turma da instituição (ex.: 3º Ano A, TSI 2024.1, etc.)
    """

    TURNO_CHOICES = [
        ("MANHA", "Manhã"),
        ("TARDE", "Tarde"),
        ("NOITE", "Noite"),
        ("INTEGRAL", "Integral"),
    ]

    codigo_turma = models.CharField(
        max_length=45,
        unique=True,
        verbose_name="Código da turma"
    )
    curso = models.CharField(
        max_length=100,
        verbose_name="Curso"
    )
    periodo = models.CharField(
        max_length=20,
        verbose_name="Período/Série"
    )
    turno = models.CharField(
        max_length=20,
        choices=TURNO_CHOICES,
        verbose_name="Turno"
    )

    usuario_admin = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="turmas_cadastradas",
        verbose_name="Usuário administrador responsável pelo cadastro"
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de cadastro"
    )

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["curso", "codigo_turma"]

    def __str__(self):
        return f"{self.codigo_turma} ({self.curso} - {self.turno})"


class Disciplina(models.Model):
    """
    Representa uma disciplina ofertada na instituição.
    """

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da disciplina"
    )
    carga_horaria = models.IntegerField(
        verbose_name="Carga horária (horas)"
    )
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )

    professor_responsavel = models.ForeignKey(
        Professor,
        on_delete=models.PROTECT,
        related_name="disciplinas_responsavel",
        verbose_name="Professor responsável"
    )

    usuario_admin = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="disciplinas_cadastradas",
        verbose_name="Usuário administrador responsável pelo cadastro"
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de cadastro"
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class HorarioAula(models.Model):
    """
    Representa um horário de aula na grade (Professor + Disciplina + Turma + dia/horário).
    Essa entidade corresponde ao HORARIO_AULA do MER/DER.
    """

    DIA_CHOICES = [
        ("SEG", "Segunda-feira"),
        ("TER", "Terça-feira"),
        ("QUA", "Quarta-feira"),
        ("QUI", "Quinta-feira"),
        ("SEX", "Sexta-feira"),
        ("SAB", "Sábado"),
    ]

    professor = models.ForeignKey(
        Professor,
        on_delete=models.PROTECT,
        verbose_name="Professor"
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.PROTECT,
        verbose_name="Disciplina"
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.PROTECT,
        verbose_name="Turma"
    )

    dia_semana = models.CharField(
        max_length=3,
        choices=DIA_CHOICES,
        verbose_name="Dia da semana"
    )
    hora_inicio = models.TimeField(
        verbose_name="Hora de início"
    )
    hora_fim = models.TimeField(
        verbose_name="Hora de término"
    )

    usuario_admin = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="horarios_cadastrados",
        verbose_name="Usuário administrador responsável pelo cadastro"
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de cadastro"
    )

    class Meta:
        verbose_name = "Horário de aula"
        verbose_name_plural = "Horários de aula"
        ordering = ["turma", "dia_semana", "hora_inicio"]

    def __str__(self):
        return f"{self.turma} - {self.disciplina} - {self.get_dia_semana_display()} {self.hora_inicio.strftime('%H:%M')}"

