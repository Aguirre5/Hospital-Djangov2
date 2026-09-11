from django.http import HttpResponse
from django.shortcuts import render, redirect
from .pacientes_db import obtener_pacientes, agregar_paciente_db
from .models import Medico
from .models import Especialidad

def saludo(request):
    return HttpResponse("Hola, bienvenido a la aplicación del hospital.")

def index(request):
    return render(request, 'app_hospital/index.html')

def pacientes(request):
    lista_pacientes = obtener_pacientes()
    return render(request, 'app_hospital/pacientes.html', {'pacientes': lista_pacientes})

def medicos(request):
    lista_medicos = Medico.objects.all()
    return render(request, 'app_hospital/medicos.html', {'medicos': lista_medicos})

def tratamientos(request):
    return render(request, 'app_hospital/tratamientos.html')

def agregar_paciente(request):
    if request.method == 'POST':
        nombre=request.POST.get('nombre', '').strip(),
        apellido=request.POST.get('apellido', '').strip(),
        dni=request.POST.get('dni', '').strip(),
        fecha_nacimiento=request.POST.get('fecha_nacimiento'),
        sexo=request.POST.get('sexo'),
        direccion=request.POST.get('direccion', '').strip(),
        telefono=request.POST.get('telefono', '').strip(),
        email=request.POST.get('email', '').strip(),
        grupo_sanguineo=request.POST.get('grupo_sanguineo', '').strip(),
        contacto_emergencia=request.POST.get('contacto_emergencia', '').strip(),
        telefono_emergencia=request.POST.get('telefono_emergencia', '').strip(),
        obra_social=request.POST.get('obra_social', '').strip(),
        numero_afiliado=request.POST.get('numero_afiliado', '').strip(),

        agregar_paciente_db(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            direccion=direccion,
            telefono=telefono,
            email=email,
            grupo_sanguineo=grupo_sanguineo,
            contacto_emergencia=contacto_emergencia,
            telefono_emergencia=telefono_emergencia,
            obra_social=obra_social,
            numero_afiliado=numero_afiliado
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