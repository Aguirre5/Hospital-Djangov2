from django.urls import path,include
from app_hospital import views

urlpatterns = [
    path('', views.index, name='index'),
    path('saludo/', views.saludo, name='saludo'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('medicos/', views.medicos, name='medicos'),
    path('tratamientos/', views.tratamientos, name='tratamientos'),
    path('pacientes/agregar/', views.agregar_paciente, name='agregar_paciente'),
    path('medicos/agregar/', views.agregar_medico, name='agregar_medico'),
]