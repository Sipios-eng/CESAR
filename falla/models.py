from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class UsuarioExtendido(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='perfil')
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol.nombre if self.rol else 'Sin Rol'}"


class Usuario(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


class EstacionSismografica(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha_instalacion = models.DateField()
    tipo = models.CharField(max_length=50, choices=[('Bajo costo', 'Bajo costo'), ('Estándar', 'Estándar')])

    def __str__(self):
        return self.nombre


class Sensor(models.Model):
    estacion = models.ForeignKey(EstacionSismografica, related_name='sensores', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=[('Temperatura', 'Temperatura'), ('Movimiento', 'Movimiento')])
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.tipo} - {self.estacion.nombre}"


class EventoSismico(models.Model):
    estacion = models.ForeignKey(EstacionSismografica, on_delete=models.CASCADE)
    magnitud = models.FloatField()
    profundidad = models.FloatField()
    epicentro = models.CharField(max_length=255)
    velocidad = models.FloatField()
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"Sismo en {self.epicentro} con magnitud {self.magnitud}"
    

class Reporte(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    analista = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    eventos_sismicos = models.ManyToManyField(EventoSismico)
    descripcion = models.TextField()

    def __str__(self):
        return f"Reporte generado por {self.analista.username if self.analista else 'Desconocido'} el {self.fecha_creacion}"


class Alerta(models.Model):
    evento = models.ForeignKey(EventoSismico, on_delete=models.CASCADE)
    analista = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Alerta para el evento {self.evento} por {self.analista.username if self.analista else 'Desconocido'}"
