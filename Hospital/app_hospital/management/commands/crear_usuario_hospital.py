"""Crear cuentas sin registro público ni contraseñas en código o línea de comandos."""
from getpass import getpass
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.db import connection, transaction, IntegrityError


class Command(BaseCommand):
    help='Crear un usuario hospitalario y asignarle un rol (SQL directo).'

    def add_arguments(self,parser):
        parser.add_argument('username')
        parser.add_argument('--nombre',required=True)
        parser.add_argument('--rol',required=True,choices=['ADMIN','MEDICO','RECEPCION','VISOR'])
        parser.add_argument('--medico-id',type=int,default=None)

    def handle(self,*args,**opts):
        username=opts['username'].strip()
        if not username or len(username)>80 or not username.replace('_','').isalnum():
            raise CommandError('Usuario: letras, números o guion bajo (máximo 80).')
        if opts['rol']=='MEDICO' and not opts['medico_id']:
            raise CommandError('El rol MEDICO requiere --medico-id de un médico existente.')
        if opts['rol']!='MEDICO' and opts['medico_id'] is not None:
            raise CommandError('--medico-id solo corresponde al rol MEDICO.')
        password=getpass('Contraseña nueva (mínimo 12 caracteres): ')
        confirmacion=getpass('Repetí la contraseña: ')
        if len(password)<12 or password != confirmacion:
            raise CommandError('Las contraseñas deben coincidir y tener al menos 12 caracteres.')
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute('SELECT id_rol FROM roles WHERE codigo=%s',[opts['rol']])
                    rol=cursor.fetchone()
                    if not rol: raise CommandError('Primero importá 001_usuarios_permisos.sql.')
                    if opts['medico_id'] is not None:
                        cursor.execute("SELECT 1 FROM medicos WHERE id_medico=%s AND estado='Activo'",
                                       [opts['medico_id']])
                        if not cursor.fetchone(): raise CommandError('Médico inexistente o inactivo.')
                    cursor.execute('''INSERT INTO usuarios(username,nombre,password_hash,id_medico)
                                      VALUES (%s,%s,%s,%s)''',
                                   [username,opts['nombre'].strip(),make_password(password),opts['medico_id']])
                    usuario_id=cursor.lastrowid
                    cursor.execute('INSERT INTO usuario_roles(id_usuario,id_rol) VALUES (%s,%s)',
                                   [usuario_id,rol[0]])
        except IntegrityError as exc:
            raise CommandError('El usuario ya existe o hay una relación inválida.') from exc
        self.stdout.write(self.style.SUCCESS(f'Cuenta {username} creada con rol {opts["rol"]}.'))
