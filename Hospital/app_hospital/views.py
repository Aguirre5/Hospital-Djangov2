from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date, datetime
import re
from .pacientes_db import obtener_pacientes, agregar_paciente_db, dni_existe
from .medicos_db import obtener_medicos, obtener_especialidades, agregar_medico_db

def saludo(request):
    return HttpResponse("Hola, bienvenido a la aplicación del hospital.")

def index(request):
    return render(request, 'app_hospital/index.html')

def pacientes(request):
    lista_pacientes = obtener_pacientes()
    return render(request, 'app_hospital/pacientes.html', {'pacientes': lista_pacientes})

def medicos(request):
    lista_medicos = obtener_medicos()
    return render(request, 'app_hospital/medicos.html', {
        'medicos': lista_medicos,})

def tratamientos(request):
    return render(request, 'app_hospital/tratamientos.html')

def agregar_paciente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        dni = request.POST.get('dni', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo_asignado_al_nacer = request.POST.get('sexo_asignado_al_nacer', '').strip()
        identidad_genero = request.POST.get('identidad_genero', '').strip()
        identidad_genero_otro = request.POST.get('identidad_genero_otro', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        grupo_sanguineo = request.POST.get('grupo_sanguineo', '').strip()
        contacto_emergencia = request.POST.get('contacto_emergencia', '').strip()
        telefono_emergencia = request.POST.get('telefono_emergencia', '').strip()
        obra_social = request.POST.get('obra_social', '').strip()
        numero_afiliado = request.POST.get('numero_afiliado', '').strip()

        #Inicio de validaciones.
        patron_nombre = r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$'

        if not nombre or not re.fullmatch(patron_nombre, nombre):
            messages.error(
                request,
                'El nombre solo puede contener letras y espacios.'
            )
            return render(
                request,
                'app_hospital/agregar_paciente.html'
            )

        if not apellido or not re.fullmatch(patron_nombre, apellido):
            messages.error(
                request,
                'El apellido solo puede contener letras y espacios.'
            )
            return render(
                request,
                'app_hospital/agregar_paciente.html'
            )

        if not dni.isdigit() or len(dni) != 8:
            messages.error(
                request,
                'El DNI debe contener exactamente 8 números.'
            )
            return render(
                request,
                'app_hospital/agregar_paciente.html'
            )

        if dni_existe(dni):
            messages.error(
                request,
                'Ya existe un paciente registrado con ese DNI.'
            )
            return render(
                request,
                'app_hospital/agregar_paciente.html'
            )

        if telefono:
            if not telefono.isdigit() or len(telefono) < 10:
                messages.error(
                    request,
                    'El teléfono debe contener solo números y tener al menos 10 dígitos.'
                )
                return render(
                    request,
                    'app_hospital/agregar_paciente.html'
                )

        if telefono_emergencia:
            if (
                not telefono_emergencia.isdigit()
                or len(telefono_emergencia) < 10
            ):
                messages.error(
                    request,
                    'El teléfono de emergencia debe contener solo números y tener al menos 10 dígitos.'
                )
                return render(
                    request,
                    'app_hospital/agregar_paciente.html'
                )

        if fecha_nacimiento:
            try:
                fecha = datetime.strptime(
                    fecha_nacimiento,
                    '%Y-%m-%d'
                ).date()

                if fecha > date.today():
                    messages.error(
                        request,
                        'La fecha de nacimiento no puede ser futura.'
                    )
                    return render(
                        request,
                        'app_hospital/agregar_paciente.html'
                    )

            except ValueError:
                messages.error(
                    request,
                    'La fecha de nacimiento no es válida.'
                )
                return render(
                    request,
                    'app_hospital/agregar_paciente.html'
                )
        
        sexos = ['M', 'F', 'I', 'N']
        identidades = ['M', 'F', 'X', 'O', 'N']
        
        if sexo_asignado_al_nacer not in sexos:
            messages.error(
                request,
                'El sexo asignado al nacer no es válido.'
            )
            return render(
                request,
                'app_hospital/agregar_paciente.html'
            )

        if identidad_genero not in identidades:
            messages.error(
                request,
                'La identidad de género no es válida.'
            )
            return render(
                request,
                'app_hospital/agregar_paciente.html'
            )
            
        if identidad_genero == 'O' and not identidad_genero_otro:
            messages.error(
                request,
                'Debe especificar la identidad de género si selecciona "Otro".'
            )
            return render(
                request,
                'app_hospital/agregar_paciente.html'
            )

        """Con esto, se protegen:
        Letras y espacios de Nombre y Apellido.
        DNI de 8 dígitos y no duplicado.
        Teléfonos de al menos 10 dígitos y solo números.
        Fecha de nacimiento no futura y válida.
        Sexo e identidad de género válidos.
        Identidad de género "Otro" requiere especificación.
        """
        
        #Acaban validaciones.
        agregar_paciente_db(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            sexo_asignado_al_nacer=sexo_asignado_al_nacer,
            identidad_genero=identidad_genero,
            identidad_genero_otro=identidad_genero_otro,
            direccion=direccion,
            telefono=telefono,
            email=email,
            grupo_sanguineo=grupo_sanguineo,
            contacto_emergencia=contacto_emergencia,
            telefono_emergencia=telefono_emergencia,
            obra_social=obra_social,
            numero_afiliado=numero_afiliado
        )
        messages.success(request, 'Paciente agregado sin problemas.')
        
        return redirect('pacientes')

    return render(request, 'app_hospital/agregar_paciente.html')

def agregar_medico(request):
    if request.method == 'POST': 
        nombre=request.POST.get('nombre', "").strip(),
        apellido=request.POST.get('apellido', "").strip(),
        matricula=request.POST.get('matricula', "").strip(),
        telefono=request.POST.get('telefono', "").strip(),
        
        email=request.POST.get('email', "").strip(),
        consultorio=request.POST.get('consultorio', "").strip(),
        horario_atencion=request.POST.get('horario_atencion', "").strip(),
        id_especialidad=request.POST.get('id_especialidad', "").strip()
        
        agregar_medico_db(
            nombre=nombre,
            apellido=apellido,
            matricula=matricula,
            telefono=telefono,
            email=email,  
            consultorio=consultorio,
            horario_atencion=horario_atencion,
            id_especialidad=id_especialidad
        )
        messages.success(request, 'Médico agregado sin problemas.')
        return redirect('medicos')

    lista_especialidades = obtener_especialidades()
    return render(request, 'app_hospital/agregar_medico.html', {'especialidades': lista_especialidades})