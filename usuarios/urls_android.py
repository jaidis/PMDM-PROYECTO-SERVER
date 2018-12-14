# -*- encoding: utf-8 -*-

__author__ = 'ruben'

from django.conf.urls import patterns, url
from usuarios import views_android as usuarios_android_views
from django.contrib.auth.decorators import login_required

urlpatterns = [url(r'^login/$', usuarios_android_views.login),
               url(r'^logout/$', usuarios_android_views.logout),
               url(r'^get_usuarios/$', usuarios_android_views.get_usuarios),
               url(r'^get_perfil/$', usuarios_android_views.get_perfil),
               url(r'^cambiar_datos/$', usuarios_android_views.cambiar_datos),
               url(r'^comprobar_token/$', usuarios_android_views.comprobar_token),
               url(r'^cambiar_pass/$', usuarios_android_views.cambiar_pass),
               url(r'^registrar_usuario/$', usuarios_android_views.registrar_usuario),
               ]
