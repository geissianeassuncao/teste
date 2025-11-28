from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PacienteViewSet, MedicoViewSet, AgendaViewSet, PeriodoViewSet, EstadoViewSet, CidadeViewSet, HorarioViewSet,
    AgendamentoViewSet, ReceitaViewSet, MedicamentoViewSet, EspecialidadeViewSet, MedicoEspecialidadeViewSet
)

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'especialidades', EspecialidadeViewSet)
router.register(r'medicoespecialidades', MedicoEspecialidadeViewSet)
router.register(r'agendas', AgendaViewSet)
router.register(r'periodos', PeriodoViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'agendamentos', AgendamentoViewSet)
router.register(r'receitas', ReceitaViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'cidades', CidadeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
