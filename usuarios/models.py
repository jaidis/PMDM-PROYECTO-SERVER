# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm
from django.db.models.signals import post_save

import os

PROJECT_PATH = os.path.dirname("__file__")

class DatosExtraUser(models.Model):
    usuario = models.OneToOneField(User)
    ciudad = models.CharField(max_length=500, blank=True, null=True)
    ciudad_actual = models.CharField(max_length=500, blank=True, null=True)
    publicidad = models.BooleanField(default=False)
    tipo = models.CharField(max_length=8, blank=False, null=False, default="django")

    def __unicode__(self):
        return u"%s" % self.usuario.username


def user_new_unicode(self):
    return self.username if self.get_full_name() == "" else self.get_full_name()

# Replace the __unicode__ method in the User class with out new implementation
User.__unicode__ = user_new_unicode


class Tokenregister(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.user.username

