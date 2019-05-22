from django.db import models
from django.contrib.auth.models import User

class Municipio(models.Model):
    nombre_municipio = models.CharField(max_length=200)
    municipio_id = models.CharField(max_length=200)
    #datos persistentes
    altitud = models.CharField(max_length=200)
    latitud = models.CharField(max_length=200)
    longitud = models.CharField(max_length=200)
    #datos variantes
    precipitaion = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    tmax = models.CharField(max_length=200)
    tmin = models.CharField(max_length=200)
    id_split = models.CharField(max_length=200)

    enlace = models.URLField(max_length = 500, null = True, blank = True)

    numcom = models.PositiveSmallIntegerField(default=0)
    puntuacion = models.PositiveSmallIntegerField(default=0)

    def  __str__(self):
        return self.nombre_municipio


class Comentario(models.Model):
    autor = models.CharField(max_length=50)
    texto = models.TextField()
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.autor + ": " + self.texto


class Usuario(models.Model):
    username = models.CharField(max_length=100, default="ejemplo")
    password = models.CharField(max_length=50, default="ejemplo")
    email = models.EmailField(max_length=100, default="example@example.com")

    colorletras = models.CharField(max_length=200)
    tamanoletras = models.PositiveSmallIntegerField(default=15)
    colorfondo = models.CharField(max_length=200)

    titulo = models.CharField(max_length=300, default="Página de usuario")

    municipios = models.ManyToManyField(Municipio)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, blank=True, null=True)
    count = models.PositiveSmallIntegerField(default=0)


    def __str__(self):
        return self.username
