#-*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Ciudad(models.Model):
    nombre = models.CharField(max_length=300)


    def __unicode__(self):
        return u"%s" % self.nombre


class Restaurante(models.Model):
    ciudad = models.ForeignKey(Ciudad)
    nombre = models.CharField(max_length=300)
    descripcion_corta = models.CharField(max_length=500)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=100)
    foto_perfil = models.ImageField(upload_to='imagenes/restaurante')
    codigoqr = models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)
    carta = models.CharField(max_length=500)

    def __unicode__(self):
        return u"%s_%s" %(self.ciudad.nombre, self.nombre)

class Valoracion(models.Model):
    usuario = models.ForeignKey(User)
    restaurante = models.ForeignKey(Restaurante)
    puntacion = models.FloatField()
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s_%s_%s_%s" %(self.restaurante.nombre, self.usuario.username, self.puntacion, self.fecha)

class Favoritos(models.Model):
    usuario = models.ForeignKey(User)
    restaurante = models.ForeignKey(Restaurante)
    favorito = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s_%s" %(self.restaurante.nombre, self.usuario.username)