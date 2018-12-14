from django.contrib import admin

# Register your models here.
from restaurantes.models import Ciudad, Restaurante, Valoracion, Favoritos

admin.site.register(Ciudad)
admin.site.register(Restaurante)
admin.site.register(Valoracion)
admin.site.register(Favoritos)