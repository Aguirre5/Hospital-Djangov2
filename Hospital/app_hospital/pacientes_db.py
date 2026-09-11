from django.db import connection

def obtener_pacientes():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT
                id_paciente,
                nombre,
                apellido,
                dni,
                fecha_nacimiento, 
                sexo,
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

def agregar_paciente_db(
    nombre,
    apellido,
    dni,
    fecha_nacimiento,
    sexo_asignado_al_nacer,
    identidad_genero,
    identidad_genero_otro,
    direccion,
    telefono,
    email,
    grupo_sanguineo,
    contacto_emergencia,
    telefono_emergencia,
    obra_social,
    numero_afiliado
):
    
    if identidad_genero in ('X', 'O'):
        sex_legacy = identidad_genero
    else:
        sex_legacy = sexo_asignado_al_nacer

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO pacientes (
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                sexo,
                sexo_asignado_al_nacer,
                identidad_genero,
                identidad_genero_otro,
                direccion,
                telefono,
                email,
                grupo_sanguineo,
                contacto_emergencia,
                telefono_emergencia,
                obra_social,
                numero_afiliado,
                `fecha_admisión`,
                estado
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                CURDATE(), 'Activo'
            )""", [
            nombre,
            apellido,
            dni,
            fecha_nacimiento,
            sex_legacy,  # Guardar el sexo asignado al nacer en la columna 'sexo'
            sexo_asignado_al_nacer,
            identidad_genero,
            identidad_genero_otro,
            direccion or None,
            telefono,
            email,
            grupo_sanguineo,
            contacto_emergencia or None,
            telefono_emergencia or None,
            obra_social or None,
            numero_afiliado or None,
        ])
        
def dni_existe(dni):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 1 FROM pacientes WHERE dni = %s LIMIT 1 """, [dni])
        return cursor.fetchone() is not None