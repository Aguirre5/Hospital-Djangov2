from django.db import connection

def obtener_medicos():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT
                m.id_medico,
                m.nombre,
                m.apellido,
                m.matricula,
                m.telefono,
                m.email,
                m.consultorio,
                m.horario_atencion,
                m.fecha_ingreso,
                m.estado,
                m.id_especialidad,
                e.nombre AS especialidad
                FROM medicos m
                INNER JOIN especialidades e ON 
                m.id_especialidad = e.id_especialidad
                ORDER BY m.apellido, m.nombre""")
        columnas = [col[0] for col in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

def obtener_especialidades():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT
                id_especialidad,
                nombre
                FROM especialidades
                ORDER BY nombre""")
        columnas = [col[0] for col in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


def agregar_medico_db (
    nombre,
    apellido,
    matricula,
    telefono,
    email,
    consultorio,
    horario_atencion,
    id_especialidad
):
    
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO medicos (
                nombre,
                apellido,
                matricula,
                telefono,
                email,
                consultorio,
                horario_atencion,
                id_especialidad,
                fecha_ingreso,
                estado
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, CURDATE(), 'Activo'
            )""", [
            nombre,
            apellido,
            matricula,
            telefono or None,
            email or None,
            consultorio,
            horario_atencion,
            id_especialidad,
        ])