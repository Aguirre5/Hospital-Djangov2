"""Vistas para autenticación granular y tratamientos; sin ORM hospitalario."""
from datetime import date
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .auth_hospital import (
    SESSION_KEY, buscar_usuario, usuario_actual, requiere_permiso, alcance_medico,
)
from .tratamientos_db import (
    listar_tratamientos, obtener_tratamiento, pacientes_disponibles,
    medicos_disponibles, crear_tratamiento, modificar_tratamiento,
)

ESTADOS = ('Pendiente','Activo','Finalizado','Suspendido')


def login_hospital(request):
    if usuario_actual(request):
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        # Mensaje genérico para no revelar la existencia de cuentas.
        usuario = buscar_usuario(username)
        if usuario and usuario['activo'] and check_password(password,usuario['password_hash']):
            request.session.flush()  # Invalida datos de sesión anteriores.
            request.session[SESSION_KEY] = usuario['id_usuario']
            request.session.set_expiry(8*60*60)
            return redirect('index')
        messages.error(request,'Usuario o contraseña incorrectos.')
    return render(request,'app_hospital/login_hospital.html')


@require_POST
def logout_hospital(request):
    request.session.flush()
    return redirect('login_hospital')


def _datos_formulario(request, editando=False):
    """Devuelve (datos, errores) sin aceptar campos clínicos no validados."""
    errores=[]
    descripcion=request.POST.get('descripcion','').strip()
    observaciones=request.POST.get('observaciones','').strip()
    estado=request.POST.get('estado','Pendiente')
    if not descripcion:
        errores.append('La descripción es obligatoria.')
    if len(descripcion)>10000 or len(observaciones)>10000:
        errores.append('La descripción y las observaciones no pueden superar 10.000 caracteres.')
    if estado not in ESTADOS:
        errores.append('Estado inválido.')

    fechas={}
    for nombre in ('fecha_inicio','fecha_fin'):
        crudo=request.POST.get(nombre,'').strip()
        if not crudo:
            fechas[nombre]=None
            continue
        try:
            fechas[nombre]=date.fromisoformat(crudo)
        except ValueError:
            fechas[nombre]=None
            errores.append(f'Fecha inválida: {nombre}.')
    if fechas['fecha_inicio'] and fechas['fecha_fin'] and fechas['fecha_fin']<fechas['fecha_inicio']:
        errores.append('La fecha de fin no puede ser anterior al inicio.')

    datos={'descripcion':descripcion,'observaciones':observaciones,
           'estado':estado,**fechas}
    if not editando:
        for campo in ('id_paciente','id_medico'):
            try:
                valor=int(request.POST.get(campo,''))
                if valor<=0: raise ValueError()
                datos[campo]=valor
            except (ValueError,TypeError):
                errores.append(f'Seleccione un {campo.replace("id_", "")} válido.')
        if not errores:
            if datos['id_paciente'] not in {p['id_paciente'] for p in pacientes_disponibles()}:
                errores.append('El paciente seleccionado no está activo o no existe.')
            if datos['id_medico'] not in {m['id_medico'] for m in medicos_disponibles()}:
                errores.append('El médico seleccionado no está activo o no existe.')
    return datos,errores


@requiere_permiso('tratamientos.ver')
def tratamientos(request):
    try:
        filtro_medico=alcance_medico(request)
    except PermissionError:
        return HttpResponseForbidden('No tiene un médico vinculado a su cuenta.')
    busqueda=request.GET.get('q','').strip()[:100]
    datos=listar_tratamientos(busqueda,filtro_medico)
    return render(request,'app_hospital/tratamientos.html',
                  {'tratamientos':datos,'busqueda':busqueda})


@requiere_permiso('tratamientos.crear')
def agregar_tratamiento(request):
    try:
        filtro_medico=alcance_medico(request)
    except PermissionError:
        return HttpResponseForbidden('No tiene un médico vinculado a su cuenta.')
    if request.method=='POST':
        datos,errores=_datos_formulario(request)
        if filtro_medico is not None and datos.get('id_medico')!=filtro_medico:
            errores.append('Solo puede registrar tratamientos a su nombre.')
        if not errores:
            crear_tratamiento(datos)
            messages.success(request,'Tratamiento registrado correctamente.')
            return redirect('tratamientos')
        for error in errores: messages.error(request,error)
    return render(request,'app_hospital/form_tratamiento.html',{
        'modo':'crear','pacientes':pacientes_disponibles(),
        'medicos':medicos_disponibles(filtro_medico),
        'estados':ESTADOS, 'datos':request.POST if request.method=='POST' else {},
    })


@requiere_permiso('tratamientos.editar')
def editar_tratamiento(request,id_tratamiento):
    try:
        filtro_medico=alcance_medico(request)
    except PermissionError:
        return HttpResponseForbidden('No tiene un médico vinculado a su cuenta.')
    actual=obtener_tratamiento(id_tratamiento,filtro_medico)
    if not actual:
        raise Http404('Tratamiento inexistente o fuera de su alcance.')
    if request.method=='POST':
        datos,errores=_datos_formulario(request,editando=True)
        if not errores:
            modificar_tratamiento(id_tratamiento,datos,filtro_medico)
            messages.success(request,'Tratamiento actualizado correctamente.')
            return redirect('tratamientos')
        for error in errores: messages.error(request,error)
    return render(request,'app_hospital/form_tratamiento.html',{
        'modo':'editar','tratamiento':actual,'estados':ESTADOS,
        'datos':request.POST if request.method=='POST' else actual,
    })
