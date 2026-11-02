from django.urls import path,include
from app_hospital import views
from app_hospital import vistas_acceso_tratamientos as vt


urlpatterns = [
    path('', views.index, name='index'),
    path('saludo/', views.saludo, name='saludo'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('medicos/', views.medicos, name='medicos'),
    path('tratamientos/', vt.tratamientos, name='tratamientos'),
    path('tratamientos/agregar/', vt.agregar_tratamiento, name='agregar_tratamiento'),
    path('tratamientos/editar/<int:id_tratamiento>/', vt.editar_tratamiento, name='editar_tratamiento'),
    path('login/', vt.login_hospital, name='login_hospital'),
    path('logout/', vt.logout_hospital, name='logout_hospital'),
    path('pacientes/agregar/', views.agregar_paciente, name='agregar_paciente'),
    path('medicos/agregar/', views.agregar_medico, name='agregar_medico'),
]