from django.shortcuts import render, redirect
from rest_framework import viewsets

from django.contrib.auth import authenticate, login

from appelderlink import models
from .models import CustomUser
from .forms import LoginForm

from .models import Agendamento

from .serializers import (
    MedicoSerializer,
    PacienteSerializer,
    ReceitaSerializer,
    AgendamentoSerializer,
    PeriodoSerializer,
    MedicamentoSerializer,
    EspecialidadeSerializer,
    AgendaSerializer,
    CidadeSerializer,
    EstadoSerializer,
    MedicoEspecialidadeSerializer,
    HorarioSerializer
)


# =====================
#       VIEWSETS
# =====================

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = models.Medico.objects.all()
    serializer_class = MedicoSerializer


class EspecialidadeViewSet(viewsets.ModelViewSet):
    queryset = models.Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer


class MedicoEspecialidadeViewSet(viewsets.ModelViewSet):
    queryset = models.MedicoEspecialidade.objects.all()
    serializer_class = MedicoEspecialidadeSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = models.Paciente.objects.all()
    serializer_class = PacienteSerializer


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = models.Agenda.objects.all()
    serializer_class = AgendaSerializer


class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = models.Periodo.objects.all()
    serializer_class = PeriodoSerializer


class HorarioViewSet(viewsets.ModelViewSet):
    queryset = models.Horario.objects.all()
    serializer_class = HorarioSerializer


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = models.Agendamento.objects.all()
    serializer_class = AgendamentoSerializer


class ReceitaViewSet(viewsets.ModelViewSet):
    queryset = models.Receita.objects.all()
    serializer_class = ReceitaSerializer


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = models.Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class EstadoViewSet(viewsets.ModelViewSet):
    queryset = models.Estado.objects.all()
    serializer_class = EstadoSerializer


class CidadeViewSet(viewsets.ModelViewSet):
    queryset = models.Cidade.objects.all()
    serializer_class = CidadeSerializer


# =====================
#       PÁGINAS
# =====================

def home(request):
    return render(request, "index.html")


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        tipo = request.POST.get("tipo")  # <--- pega se é medico ou paciente
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if user.tipo == "paciente":
                    return redirect("paciente_home")

                elif user.tipo == "medico":
                    return redirect("medico_home")

                return redirect("home")

            return render(request, "index.html", {
                "erro": "Usuário ou senha incorretos.",
                "form": form
            })

    return render(request, "index.html", {"form": form})



def paciente_home(request):
    agendamentos = Agendamento.objects.filter(paciente__user=request.user)
    return render(request, "paciente_home.html", {
        "agendamentos": agendamentos
    })


def medico_home(request):
    return render(request, "medico_home.html")
