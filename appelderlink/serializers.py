from rest_framework import serializers
from appelderlink import models

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medico
        field = '__al__'

class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Especialidade
        field = '__al__'

class MedicoEspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicoEspecialidade
        field = '__al__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paciente
        field = '__al__'

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agenda
        field = '__al__'

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Periodo
        field = '__al__'

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Horario
        field = '__al__'

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agendamento
        field = '__al__'

class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Receita
        field = '__al__'

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medicamento
        field = '__al__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Estado
        field = '__al__'


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cidade
        field = '__al__'



