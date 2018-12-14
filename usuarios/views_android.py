# -*- encoding: utf-8 -*-
__author__ = 'ruben'

import django.contrib.auth as auth
import django.http as http
from annoying.functions import get_object_or_None
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import datetime
from utilidades import Token
from usuarios.models import Tokenregister, DatosExtraUser
from django.contrib.auth.models import User


# definicion para conseguir el usuario de django a partir del token
def get_userdjango_by_token(datos):
    token = datos.get('token')
    user_token = Tokenregister.objects.get(token=token)
    return user_token.user


# definicion para conseguir el usuario de django a partir del id de usuario
def get_userdjango_by_id(datos):
    userdjango_id = datos.get('usuario_id')
    userdjango = get_object_or_None(User, pk=userdjango_id)
    return userdjango


# definicion para comprobar el usuario
def comprobar_usuario(datos):
    userdjango = get_userdjango_by_id(datos)
    user_token = get_userdjango_by_token(datos)

    if (user_token is not None) and (userdjango is not None):
        if user_token == userdjango:
            return True
        else:
            return False


# definicion para loguear un usuario desde la aplicación java
@csrf_exempt
def login(request):
    print "Login"
    try:
        datos = json.loads(request.POST['data'])
        us = datos.get('usuario').lower()
        password = datos.get('password')

        if (us is None and password is None) or (us == "" and password == ""):
            response_data = {'result': 'error', 'message': 'Falta el usuario y el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if us is None or us == "":
            response_data = {'result': 'error', 'message': 'Falta el usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None or password == "":
            response_data = {'result': 'error', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        user = auth.authenticate(username=us, password=password)

        if user is not None:
            if user.is_active:
                user_token = get_object_or_None(Tokenregister, user=user)

                if user_token is None:
                    token1 = str(user.id) + "_" + Token.id_generator()
                    tokenform = Tokenregister(token=token1, user=user)
                    tokenform.save()
                    user_token = get_object_or_None(Tokenregister, user=user)
                    response_data = {'result': 'ok', 'message': 'Usuario logueado', 'token': user_token.token,
                                     'usuario': user.username,
                                     'nombre': user.first_name,
                                     }
                else:
                    # user_token.date = datetime.datetime.now()
                    # user_token.token = str(user.id) + "_" + Token.id_generator()
                    # user_token.save()
                    user_token.delete()
                    token1 = str(user.id) + "_" + Token.id_generator()
                    tokenform = Tokenregister(token=token1, user=user)
                    tokenform.save()
                    user_token = get_object_or_None(Tokenregister, user=user)

                    response_data = {'result': 'ok', 'message': 'Token Regenerado', 'token': user_token.token,
                                     'usuario': user.username,
                                     'nombre': user.first_name
                                     }

                return http.HttpResponse(json.dumps(response_data), content_type="application/json")

            else:
                response_data = {'result': 'error', 'message': 'Usuario no activo'}
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {'result': 'error', 'message': 'Usuario no válido'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0001', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# definicion para logear un usuario desde la aplicación java
@csrf_exempt
def logout(request):
    print "Logout"
    try:
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)

            user_token = get_object_or_None(Tokenregister, user=userdjango)
            if user_token is None:
                response_data = {'result': 'ok', 'message': 'Usuario ya deslogueado'}
            else:
                user_token.delete()
                response_data = {'result': 'ok', 'message': 'Usuario ya deslogueado'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# definicion para comprobar el token
@csrf_exempt
def comprobar_token(request):
    print "Comprobando token"
    try:
        datos = json.loads(request.POST['data'])
        token = datos.get('token')
        print datos
        if token != "" and comprobar_usuario(datos):
            response_data = {'result': 'ok', 'message': 'Usuario logueado'}

        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0003', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_perfil(request):
    print "buscando perfil"
    try:
        datos = json.loads(request.POST['data'])

        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)

            response_data = {'result': 'ok', 'message': 'Perfil de usuario',
                             'email': userdjango.email,
                             'username': userdjango.username,
                             'nombre': userdjango.first_name,
                             'apellidos': userdjango.last_name}

        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0004', 'result': 'error', 'message': 'Error en perfil de usuario: '+str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


# metodo para que un usuario pueda ver su perfil, necesario estar loegueado y pasar su id y token
@csrf_exempt
def cambiar_pass(request):
    print "cambiando pass"
    try:
        datos = json.loads(request.POST['data'])
        antiguapass = datos.get('antigua')
        nuevapass = datos.get('nueva')

        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)
            if userdjango.check_password(antiguapass):
                userdjango.set_password(nuevapass)
                userdjango.save()
                token = get_object_or_None(Tokenregister, user=userdjango)
                token.delete()
                response_data = {'result': 'ok', 'message': 'Password cambiado'}
            else:
                response_data = {'result': 'error', 'message': 'Password antiguo incorrecto'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error', 'message': 'Error en perfil de usuario: '+str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_datos(request):
    print "cambiando pass"
    try:
        datos = json.loads(request.POST['data'])
        if comprobar_usuario(datos):
            userdjango = get_userdjango_by_token(datos)
            userdjango.first_name = datos.get('nombre')
            userdjango.last_name = datos.get('apellidos')
            userdjango.email = datos.get('email')
            userdjango.save()
            response_data = {'result': 'ok', 'message': 'Datos cambiados'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0007', 'result': 'error', 'message': 'Error en perfil de usuario: '+str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def get_usuarios(request):
    print "buscando usuarios"
    try:
        # datos = json.loads(request.POST['data'])

        # if comprobar_usuario(datos):
        response_data = {'result': 'ok', 'message': 'Listado de usuarios', 'usuarios': []}
        usuarios = User.objects.all().order_by('id')
        for a in usuarios:
            response_data['usuarios'].append({'pk': a.pk, 'username': a.username, 'email': a.email, })

        # else:
        #     response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0006', 'result': 'error', 'message': 'Error en busqueda de usuarios : '+str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

# realizar este get_usuarios en Centros y Sesiones. Lo unico que varia es el try con los datos que cada uno pide
# el de centros realizarlo en view_java de Centros



# definicion para registrar un usuario
@csrf_exempt
def registrar_usuario(request):
    print "registrando usuario"
    data = request.POST
    print data

    try:
        datos = json.loads(request.POST['data'])
        print datos

        nombre = datos.get('usuario')
        email = datos.get('email')
        os_user = datos.get('os_user')
        # os_registration=datos.get('os_registration')
        password = datos.get('password')
        ciudad = datos.get('ciudad')
        publicidad = datos.get('publicidad')

        if (nombre is None and email is None and password is None) or (nombre == "" and password == "" and email == ""):
            response_data = {'result': 'error', 'message': 'Falta el nombre usuario, email y password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if nombre is None or nombre == "":
            response_data = {'result': 'error', 'message': 'Falta el nombre de usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None or password == "":
            response_data = {'result': 'error', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if email is None or email == "":
            response_data = {'result': 'error', 'message': 'Falta el email'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        usuarios = User.objects.filter(username=nombre)
        usuarios_email = User.objects.filter(email=email)

        if usuarios.count() == 0:
            if usuarios_email.count() == 0:
                user = User.objects.create(username=nombre, email=email)
                user.set_password(password)
                usuario = DatosExtraUser.objects.create(usuario=user, ciudad=ciudad, ciudad_actual="", publicidad=publicidad)
                user.save()
                usuario.save()
                response_data = {'result': 'ok', 'message': 'Usuario creado correctamente'}
            else:
                response_data = {'result': 'error', 'message': 'Este email ya existe'}
        else:
            response_data = {'result': 'error', 'message': 'Este nombre de usuario ya existe'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': data, 'result': 'error', 'message': 'Error en crear usuario. ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")




@csrf_exempt
def registrar_usuario_facebook_google(request):
    ##print "registrando usuario"
    try:
        datos = json.loads(request.POST['data'])
        email = datos.get('email')
        tipo = datos.get("tipo")
        nickText = datos.get('nick')
        nombre = datos.get('nombre')
        os_user = datos.get('os_user')
        apellidos = datos.get("apellidos")
        # password = datos.get('password')

        if email is None or email == "":
            response_data = {'result': 'error', 'message': 'Falta el email'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        usuarios = User.objects.filter(username=email)
        usuarios_email = User.objects.filter(email=email)

        if usuarios.count() == 0:
            if usuarios_email.count() == 0:
                if (nombre is not None and apellidos is not None):
                    user = User.objects.create(username=email, email=email, first_name=nombre, last_name=apellidos)
                else:
                    user = User.objects.create(username=email, email=email)
                user.set_password("")
                if (os_user != "" and os_user is not None):
                    usuario = DatosExtraUser.objects.create(user=user, nick=nickText, direccion="", telefono="",
                                                            tipo=tipo, onesignal_id=os_user)
                else:
                    usuario = DatosExtraUser.objects.create(user=user, nick=nickText, direccion="", telefono="",
                                                            tipo=tipo)
                user.save()
                usuario.save()
                ##print "todo ok"
                response_data = {'result': 'ok', 'message': 'Usuario creado correctamente'}
            else:
                response_data = {'result': 'error', 'message': 'Este email ya existe'}
        else:
            response_data = {'result': 'error', 'message': 'Este nombre de usuario ya existe'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error', 'message': 'Error en crear usuario. ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")