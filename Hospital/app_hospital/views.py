from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Paciente
from .models import Medico
from .models import Especialidad


def saludo(request):
    return HttpResponse('Hola Mundo')

def index(request):
    return render(request, 'app_hospital/index.html')

def pacientes(request):
    lista_pacientes = Paciente.objects.all()
    return render(request, 'app_hospital/pacientes.html', {'pacientes': lista_pacientes})

def medicos(request):
    lista_medicos = Medico.objects.all()
    return render(request, 'app_hospital/medicos.html', {'medicos': lista_medicos})

def tratamientos(request):
    return render(request, 'app_hospital/tratamientos.html')

def agregar_paciente(request):
    if request.method == 'POST':
        Paciente.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            dni=request.POST.get('dni'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento'),
            sexo=request.POST.get('sexo'),
            telefono=request.POST.get('telefono'),
            estado=request.POST.get('estado'),
        )
        return redirect('pacientes')

    return render(request, 'app_hospital/agregar_paciente.html')

def agregar_medico(request):
    if request.method == 'POST':
        Medico.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            matricula=request.POST.get('matricula'),
            telefono=request.POST.get('telefono'),
            id_especialidad_id=request.POST.get('id_especialidad'),
            estado=request.POST.get('estado'),
        )
        return redirect('medicos')

    lista_especialidades = Especialidad.objects.all()
    return render(request, 'app_hospital/agregar_medico.html', {'especialidades': lista_especialidades})