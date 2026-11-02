"""Autenticación local con SQL directo (sin ORM hospitalario).

La sesión guarda únicamente un ID. Roles y permisos se consultan en cada request;
si se revoca un permiso o se desactiva un usuario, se aplica inmediatamente.
"""
from functools import wraps
from django.db import connection
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

SESSION_KEY = 'hospital_usuario_id'


def buscar_usuario(username):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id_usuario, username, nombre, password_hash, activo "
            "FROM usuarios WHERE username=%s LIMIT 1", [username]
        )
        fila = cursor.fetchone()
    if not fila:
        return None
    return dict(zip(('id_usuario','username','nombre','password_hash','activo'), fila))


def usuario_actual(request):
    if hasattr(request, '_hospital_usuario'):
        return request._hospital_usuario
    usuario_id = request.session.get(SESSION_KEY)
    if not usuario_id:
        request._hospital_usuario = None
        return None
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id_usuario,username,nombre,id_medico FROM usuarios "
            "WHERE id_usuario=%s AND activo=1", [usuario_id]
        )
        fila = cursor.fetchone()
        if not fila:
            request.session.flush()
            request._hospital_usuario = None
            return None
        usuario = dict(zip(('id_usuario','username','nombre','id_medico'),fila))
        cursor.execute(
            "SELECT r.codigo FROM usuario_roles ur JOIN roles r ON r.id_rol=ur.id_rol "
            "WHERE ur.id_usuario=%s", [usuario_id]
        )
        usuario['roles'] = {fila[0] for fila in cursor.fetchall()}
        cursor.execute(
            "SELECT DISTINCT p.codigo FROM usuario_roles ur "
            "JOIN rol_permisos rp ON rp.id_rol=ur.id_rol "
            "JOIN permisos p ON p.id_permiso=rp.id_permiso "
            "WHERE ur.id_usuario=%s", [usuario_id]
        )
        permisos = {fila[0] for fila in cursor.fetchall()}
        cursor.execute(
            "SELECT p.codigo,up.permitido FROM usuario_permisos up "
            "JOIN permisos p ON p.id_permiso=up.id_permiso "
            "WHERE up.id_usuario=%s", [usuario_id]
        )
        for codigo, permitido in cursor.fetchall():
            if permitido:
                permisos.add(codigo)
            else:
                permisos.discard(codigo)
        usuario['permisos'] = permisos
    request._hospital_usuario = usuario
    return usuario


def tiene_permiso(request, codigo):
    usuario = usuario_actual(request)
    return bool(usuario and codigo in usuario['permisos'])


def requiere_permiso(codigo):
    def decorar(vista):
        @wraps(vista)
        def wrapper(request, *args, **kwargs):
            usuario = usuario_actual(request)
            if not usuario:
                return redirect('login_hospital')
            if codigo not in usuario['permisos']:
                return HttpResponseForbidden('No tiene permiso para realizar esta operación.')
            return vista(request, *args, **kwargs)
        return wrapper
    return decorar


def contexto_permisos(request):
    usuario = usuario_actual(request)
    return {'usuario_hospital': usuario,
            'permisos_hospital': usuario['permisos'] if usuario else set()}


def alcance_medico(request):
    """None = administrador con acceso global; int = médico propio.
    Si no tiene médico asignado, se deniega; nunca se devuelve acceso global por omisión.
    """
    usuario = usuario_actual(request)
    if usuario and 'ADMIN' in usuario['roles']:
        return None
    if not usuario or usuario['id_medico'] is None:
        raise PermissionError('El usuario no tiene médico asociado.')
    return int(usuario['id_medico'])
