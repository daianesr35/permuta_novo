from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validar_cpf(value):
    """
    Valida um CPF brasileiro.

    - Aceita com ou sem pontuação (000.000.000-00 ou 00000000000)
    - Verifica se tem 11 dígitos numéricos
    - Rejeita sequências repetidas (111.111.111-11, 000... etc.)
    - Confere os dois dígitos verificadores
    """
    cpf = "".join(ch for ch in str(value) if ch.isdigit())

    # 1) Tamanho
    if len(cpf) != 11:
        raise ValidationError("CPF deve ter exatamente 11 dígitos numéricos.")

    # 2) Sequência repetida (11111111111, 00000000000 etc.)
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    # 3) Cálculo dos dígitos verificadores
    def calcula_digito(cpf_parcial):
        soma = 0
        peso = len(cpf_parcial) + 1
        for caractere in cpf_parcial:
            soma += int(caractere) * peso
            peso -= 1
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    dv1 = calcula_digito(cpf[:9])
    dv2 = calcula_digito(cpf[:9] + dv1)

    if cpf[-2:] != dv1 + dv2:
        raise ValidationError("CPF inválido.")

    # Se chegou até aqui, é válido
    return value


def validar_telefone(value):
    """
    Valida telefone brasileiro de forma simples:

    - Aceita com ou sem formatação: (87) 9 9999-9999, 87999999999, etc.
    - Remove tudo que não for dígito
    - Considera válido se tiver 10 ou 11 dígitos (com ou sem 9 na frente)
    - Permite vazio, pois o campo é opcional (blank=True)
    """
    texto = str(value).strip()
    if not texto:
        # Campo opcional: se vier vazio, não valida nada
        return value

    digitos = "".join(ch for ch in texto if ch.isdigit())

    if len(digitos) < 10 or len(digitos) > 11:
        raise ValidationError(
            "Telefone deve ter DDD + número (10 ou 11 dígitos, ex: (87) 9999-9999 ou (87) 9 9999-9999)."
        )

    return value


class Professor(models.Model):
    """
    Representa o professor da instituição, ligado a um usuário do sistema (User).
    Esse model corresponde à entidade PROFESSOR do MER/DER.
    """

    # Usuário que faz login no sistema (tabela USUARIO no MER/DER)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professor",
        verbose_name="Usuário do sistema"
    )

    # Campos específicos do professor (como no MER/DER)
    matricula_siape = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Matrícula SIAPE"
    )

    cpf = models.CharField(
        max_length=14,  # permite "000.000.000-00" ou só números
        unique=True,
        verbose_name="CPF",
        validators=[validar_cpf],
        help_text="Informe um CPF válido, com ou sem pontuação."
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone",
        validators=[validar_telefone],
        help_text="Informe DDD + número (ex.: (87) 9 9999-9999)."
    )

    coordenacao = models.CharField(
        max_length=100,
        verbose_name="Coordenação"
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de cadastro"
    )

    # Usuário ADMIN que cadastrou esse professor
    usuario_admin = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="professores_cadastrados",
        verbose_name="Usuário administrador responsável pelo cadastro"
    )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - SIAPE: {self.matricula_siape}"

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ["user__first_name", "user__last_name"]

    @property
    def nome(self):
        """
        Atalho para o nome completo do professor.
        Usa o nome completo do User; se não tiver, usa o username.
        """
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return f"{self.nome} ({self.matricula_siape})"
