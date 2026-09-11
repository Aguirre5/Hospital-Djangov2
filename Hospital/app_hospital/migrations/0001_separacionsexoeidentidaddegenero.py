from django.db import migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE pacientes
            ADD COLUMN sexo_asignado_al_nacer CHAR(1) NOT NULL DEFAULT 'N' AFTER fecha_nacimiento;""", 
            reverse_sql="""
            ALTER TABLE pacientes
            DROP COLUMN sexo_asignado_al_nacer;
            """
        ),
        
        migrations.RunSQL(
            sql="""
            ALTER TABLE pacientes
            ADD COLUMN identidad_genero CHAR(1) NOT NULL DEFAULT 'N' AFTER sexo_asignado_al_nacer;
            """,
            reverse_sql="""
            ALTER TABLE pacientes
            DROP COLUMN identidad_genero;
            """
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE pacientes
                ADD COLUMN identidad_genero_otro VARCHAR(100) NULL
                AFTER identidad_genero;
            """,
            reverse_sql="""
                ALTER TABLE pacientes
                DROP COLUMN identidad_genero_otro;
            """
        ),

        migrations.RunSQL(
            sql="""
                UPDATE pacientes
                SET
                    sexo_asignado_al_nacer =
                        CASE
                            WHEN sexo IN ('M', 'F', 'I')
                                THEN sexo
                            ELSE 'N'
                        END,

                    identidad_genero =
                        CASE
                            WHEN sexo = 'X' THEN 'X'
                            WHEN sexo = 'O' THEN 'O'
                            ELSE 'N'
                        END;
            """,
            reverse_sql=migrations.RunSQL.noop
        ),
    ]