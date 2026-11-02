"""Conceder o revocar permisos específicos sin cambiar el rol.
Ejemplo: python manage.py permiso_usuario_hospital ana tratamientos.ver permitir
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help='Conceder, denegar o restaurar un permiso individual de un usuario.'
    def add_arguments(self,parser):
        parser.add_argument('username')
        parser.add_argument('permiso')
        parser.add_argument('accion',choices=['permitir','denegar','restaurar'])

    def handle(self,*args,**opts):
        with connection.cursor() as cursor:
            cursor.execute('SELECT id_usuario FROM usuarios WHERE username=%s',[opts['username']])
            u=cursor.fetchone()
            cursor.execute('SELECT id_permiso FROM permisos WHERE codigo=%s',[opts['permiso']])
            p=cursor.fetchone()
            if not u or not p: raise CommandError('Usuario o permiso no encontrado.')
            if opts['accion']=='restaurar':
                cursor.execute('DELETE FROM usuario_permisos WHERE id_usuario=%s AND id_permiso=%s',
                               [u[0],p[0]])
            else:
                cursor.execute('''INSERT INTO usuario_permisos(id_usuario,id_permiso,permitido)
                                  VALUES (%s,%s,%s)
                                  ON DUPLICATE KEY UPDATE permitido=VALUES(permitido)''',
                               [u[0],p[0],1 if opts['accion']=='permitir' else 0])
        self.stdout.write(self.style.SUCCESS('Permiso actualizado.'))
