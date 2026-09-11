from django.db import connection

def obtener_pacientes():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT
                id_paciente,
                nombre,
                apellido,
                dni,
                fecha_nacimiento, sexo,
                direccion,
                telefono,
                email,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                obra_social,
                numero_afiliado,
                fecha_admisión AS fecha_admision,
                estado
                FROM pacientes ORDER BY apellido, nombre""")
        columnas = [col[0] for col in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]