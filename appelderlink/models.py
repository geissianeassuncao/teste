from django.db import models
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# ------------------------------------------------------------
#  CUSTOM USER (novo modelo de usuário)
# ------------------------------------------------------------
class CustomUser(AbstractUser):
    TIPOS = (
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
    )

    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return f"{self.username} ({self.tipo})"


# ------------------------------------------------------------
#  MODELO BASE
# ------------------------------------------------------------
class ModeloBase(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ------------------------------------------------------------
#  ENDEREÇO: ESTADO E CIDADE
# ------------------------------------------------------------
class Estado(ModeloBase):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f"{self.nome} - {self.sigla}"

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'


class Cidade(ModeloBase):
    nome = models.CharField(max_length=150)

    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        related_name='cidades'
    )

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        constraints = [
            models.UniqueConstraint(fields=['nome', 'estado'], name='unique_cidade_estado')
        ]

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"


# ------------------------------------------------------------
#  MÉDICO
# ------------------------------------------------------------
class Medico(ModeloBase):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    senha = models.CharField(max_length=100, default="1234")

    def __str__(self):
        return self.user.first_name or self.user.username

    class Meta:
        verbose_name = 'Medico'
        verbose_name_plural = 'Medicos'


# ------------------------------------------------------------
#  ESPECIALIDADE
# ------------------------------------------------------------
class Especialidade(ModeloBase):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'


class MedicoEspecialidade(ModeloBase):
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE
    )
    especialidade = models.ForeignKey(
        Especialidade,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.medico} - {self.especialidade}"

    class Meta:
        verbose_name = "MedicoEspecialidade"
        verbose_name_plural = "MedicoEspecialidades"


# ------------------------------------------------------------
#  PACIENTE
# ------------------------------------------------------------
class Paciente(ModeloBase):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    telefone = models.CharField(max_length=20, null=True, blank=True)
    idade = models.IntegerField()
    rua = models.CharField(max_length=200)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=150)
    cep = models.CharField(max_length=20)
    referencia = models.TextField(null=True, blank=True)

    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.CASCADE,
        related_name="pacientes"
    )

    def __str__(self):
        return self.user.first_name or self.user.username

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'


# ------------------------------------------------------------
#  AGENDA E PERIODOS
# ------------------------------------------------------------
class Agenda(ModeloBase):
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="agendas"
    )
    data_inicial = models.DateField()
    data_final = models.DateField()
    duracao_consulta = models.IntegerField(default=30)

    def __str__(self):
        return f"Agenda de {self.medico} ({self.data_inicial} a {self.data_final})"


class Periodo(ModeloBase):
    agenda = models.ForeignKey(
        Agenda,
        on_delete=models.CASCADE,
        related_name="periodos"
    )
    inicio = models.TimeField(default=time(8, 0))
    fim = models.TimeField(default=time(22, 0))

    def __str__(self):
        return f"{self.inicio} - {self.fim} ({self.agenda.medico})"

    def gerar_horarios(self):
        from .models import Horario

        if not self.fim:
            return []

        data_atual = self.agenda.data_inicial
        horarios_criados = []
        duracao = timedelta(minutes=self.agenda.duracao_consulta)

        tz = timezone.get_current_timezone() if getattr(settings, "USE_TZ", False) else None

        while data_atual <= self.agenda.data_final:
            inicio_dia = datetime.combine(data_atual, self.inicio)
            fim_dia = datetime.combine(data_atual, self.fim)

            if tz and timezone.is_naive(inicio_dia):
                inicio_dia = timezone.make_aware(inicio_dia, tz)
                fim_dia = timezone.make_aware(fim_dia, tz)

            horario_inicio = inicio_dia

            while horario_inicio + duracao <= fim_dia:
                horario_fim = horario_inicio + duracao

                horario_obj, criado = Horario.objects.get_or_create(
                    periodo=self,
                    inicio=horario_inicio,
                    fim=horario_fim,
                    defaults={"disponivel": True},
                )

                horarios_criados.append(horario_obj)
                horario_inicio = horario_fim

            data_atual += timedelta(days=1)

        return horarios_criados


# ------------------------------------------------------------
#  HORÁRIOS E AGENDAMENTOS
# ------------------------------------------------------------
class Horario(ModeloBase):
    periodo = models.ForeignKey(
        Periodo,
        on_delete=models.CASCADE,
        related_name="horarios"
    )
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.inicio:%d/%m %H:%M} - {self.fim:%H:%M}"


class Agendamento(ModeloBase):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="agendamentos"
    )
    horario = models.OneToOneField(
        Horario,
        on_delete=models.CASCADE,
        related_name="agendamento",
        null=True,
        blank=True
    )

    def __str__(self):
        if self.horario:
            return f"{self.paciente} - {self.horario.inicio:%d/%m %H:%M}"
        return f"{self.paciente} (sem horário definido)"

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"


# ------------------------------------------------------------
#  RECEITAS E MEDICAMENTOS
# ------------------------------------------------------------
class Receita(ModeloBase):
    data = models.DateTimeField(auto_now_add=True)
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="receitas"
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="receitas"
    )

    def __str__(self):
        return f"Receita de {self.medico} para {self.paciente} ({self.data:%d/%m/%Y})"


class Medicamento(ModeloBase):
    receita = models.ForeignKey(
        Receita,
        on_delete=models.CASCADE,
        related_name="medicamentos"
    )
    nome = models.CharField(max_length=100)
    dosagem = models.CharField(max_length=100)
    tem_em_casa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.dosagem}"
