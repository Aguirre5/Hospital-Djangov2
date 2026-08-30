from django.db import models

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    grupo_sanguineo = models.CharField(max_length=5, null=True, blank=True)
    contacto_emergencia = models.CharField(max_length=100, null=True, blank=True)
    telefono_emergencia = models.CharField(max_length=30, null=True, blank=True)
    obra_social = models.CharField(max_length=100, null=True, blank=True)
    numero_afiliado = models.CharField(max_length=50, null=True, blank=True)
    fecha_alta = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'pacientes'  

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        managed = False
        db_table = 'especialidades'

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    consultorio = models.CharField(max_length=50, null=True, blank=True)
    horario_atencion = models.CharField(max_length=255, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.DO_NOTHING, db_column='id_especialidad')

    class Meta:
        managed = False
        db_table = 'medicos'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'