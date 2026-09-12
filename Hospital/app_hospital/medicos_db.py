from django.db import connection

def obtener_medicos(busqueda=''):
    with connection.cursor() as cursor:
        sql="""SELECT
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
                """
        
        parametros = []

        if busqueda:

            termino = f"%{busqueda}%"

            sql += """
                WHERE
                    CAST(m.id_medico AS CHAR) LIKE %s
                    OR m.nombre LIKE %s
                    OR m.apellido LIKE %s
                    OR CONCAT(m.nombre, ' ', m.apellido) LIKE %s
                    OR m.matricula LIKE %s
                    OR e.nombre LIKE %s
            """

            parametros = [
                termino,
                termino,
                termino,
                termino,
                termino,
                termino,
            ]

        sql += """
            ORDER BY m.apellido, m.nombre
        """

        cursor.execute(sql, parametros)

        columnas = [col[0] for col in cursor.description]
        filas = cursor.fetchall()
    return [dict(zip(columnas, fila)) for fila in filas]

def obtener_especialidades():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT
                id_especialidad,
                nombre
                FROM especialidades
                ORDER BY nombre""")
        columnas = [col[0] for col in cursor.description]
        filas = cursor.fetchall()
    return [dict(zip(columnas, fila)) for fila in filas]




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
            consultorio or None,
            horario_atencion or None,
            id_especialidad,
        ])