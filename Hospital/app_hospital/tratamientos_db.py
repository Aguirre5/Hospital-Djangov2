"""CRUD de tratamientos con consultas SQL parametrizadas (sin ORM)."""
from django.db import connection


def _diccionarios(cursor):
    nombres = [c[0] for c in cursor.description]
    return [dict(zip(nombres,fila)) for fila in cursor.fetchall()]


def listar_tratamientos(busqueda='', id_medico=None):
    sql = """SELECT t.id_tratamiento,t.descripcion,t.fecha_prescripcion,
                    t.fecha_inicio,t.fecha_fin,t.estado,t.observaciones,
                    t.id_paciente,t.id_medico,
                    CONCAT(p.nombre, ' ', p.apellido) AS paciente,
                    CONCAT(m.nombre, ' ', m.apellido) AS medico
             FROM tratamientos t
             JOIN pacientes p ON p.id_paciente=t.id_paciente
             JOIN medicos m ON m.id_medico=t.id_medico
             WHERE 1=1"""
    parametros = []
    if id_medico is not None:
        sql += " AND t.id_medico=%s"
        parametros.append(id_medico)
    if busqueda:
        sql += """ AND (CAST(t.id_tratamiento AS CHAR) LIKE %s
                     OR p.nombre LIKE %s OR p.apellido LIKE %s
                     OR CONCAT(p.nombre,' ',p.apellido) LIKE %s
                     OR m.nombre LIKE %s OR m.apellido LIKE %s
                     OR t.descripcion LIKE %s OR t.estado LIKE %s)"""
        parametros.extend([f'%{busqueda}%']*8)
    sql += ' ORDER BY t.id_tratamiento DESC'
    with connection.cursor() as cursor:
        cursor.execute(sql,parametros)
        return _diccionarios(cursor)


def obtener_tratamiento(id_tratamiento,id_medico=None):
    sql = """SELECT t.*,CONCAT(p.nombre,' ',p.apellido) AS paciente,
                       CONCAT(m.nombre,' ',m.apellido) AS medico
             FROM tratamientos t
             JOIN pacientes p ON p.id_paciente=t.id_paciente
             JOIN medicos m ON m.id_medico=t.id_medico
             WHERE t.id_tratamiento=%s"""
    params=[id_tratamiento]
    if id_medico is not None:
        sql+=' AND t.id_medico=%s'
        params.append(id_medico)
    with connection.cursor() as cursor:
        cursor.execute(sql,params)
        datos=_diccionarios(cursor)
    return datos[0] if datos else None


def pacientes_disponibles():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id_paciente,CONCAT(nombre,' ',apellido) AS nombre
                          FROM pacientes WHERE estado='Activo' ORDER BY apellido,nombre""")
        return _diccionarios(cursor)


def medicos_disponibles(id_medico=None):
    sql="""SELECT id_medico,CONCAT(nombre,' ',apellido) AS nombre
           FROM medicos WHERE estado='Activo'"""
    params=[]
    if id_medico is not None:
        sql+=' AND id_medico=%s'
        params.append(id_medico)
    sql+=' ORDER BY apellido,nombre'
    with connection.cursor() as cursor:
        cursor.execute(sql,params)
        return _diccionarios(cursor)


def crear_tratamiento(datos):
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO tratamientos
            (id_paciente,id_medico,descripcion,fecha_prescripcion,fecha_inicio,
             fecha_fin,estado,observaciones)
            VALUES (%s,%s,%s,CURDATE(),%s,%s,%s,%s)""",
            [datos['id_paciente'],datos['id_medico'],datos['descripcion'],
             datos['fecha_inicio'],datos['fecha_fin'],datos['estado'],datos['observaciones']])
        return cursor.lastrowid


def modificar_tratamiento(id_tratamiento,datos,id_medico=None):
    # No se modifica quién es paciente o médico de un tratamiento existente.
    sql="""UPDATE tratamientos SET descripcion=%s,fecha_inicio=%s,fecha_fin=%s,
           estado=%s,observaciones=%s WHERE id_tratamiento=%s"""
    params=[datos['descripcion'],datos['fecha_inicio'],datos['fecha_fin'],
            datos['estado'],datos['observaciones'],id_tratamiento]
    if id_medico is not None:
        sql+=' AND id_medico=%s'
        params.append(id_medico)
    with connection.cursor() as cursor:
        cursor.execute(sql,params)
