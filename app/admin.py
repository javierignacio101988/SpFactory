from django.contrib import admin
from .models import Marca, Producto, Contacto


class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "marca", "precio"]
    list_editable = ["precio", "marca"]
    search_fields = ["nombre"]
    list_filter = ["marca", "precio"]



admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto)