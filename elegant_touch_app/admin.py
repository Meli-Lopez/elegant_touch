from django.contrib import admin
from .models import (PerfilUsuario, Cliente, Proveedor, Marca, Categoria, Producto, MetodoDePago, Reseña, Contacto, Subcategoria, GestionCategoria, Inventario, PedidoCliente)
from django.utils.html import mark_safe

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria__nombre')

@admin.register(GestionCategoria)
class GestionCategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'subcategoria', 'usuario', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('categoria', 'usuario')
    search_fields = ('categoria__nombre', 'subcategoria__nombre', 'usuario__username')
    date_hierarchy = 'fecha_creacion'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('perfil_usuario',)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'correo_cliente', 'direccion', 'telefono')



@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_proveedor', 'apellido_proveedor', 'telefono_proveedor', 'correo_proveedor')

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre_marca',)
    search_fields = ('nombre_marca',) 


@admin.register(MetodoDePago)
class MetodoDePagoAdmin(admin.ModelAdmin):
    list_display = ('nombre_metodo_pago',)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'direccion', 'mensaje')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio_producto', 'stock_producto', 'es_nuevo', 'destacado')
    search_fields = ('nombre_producto',)
    list_filter = ('marca', 'categoria', 'es_nuevo', 'destacado')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('user', 'producto', 'titulo', 'calificacion', 'fecha_creacion')  # Muestra estos campos en la lista
    list_filter = ('calificacion', 'fecha_creacion')  # Filtros para calificación y fecha
    search_fields = ('user__username', 'producto__nombre_producto', 'titulo')  # Campos de búsqueda
    

admin.site.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'descripcion', 'precio', 'stock', 'proveedor', 'agotado', 'mostrar_imagen_producto', 'fecha_actualizacion', 'cantidad_minima', 'cantidad_maxima')

    def mostrar_imagen_producto(self, obj):
        # Verifica si el producto tiene imágenes asociadas
        imagen_producto = obj.producto.imagenes.first()  # Usando el related_name 'imagenes' del Producto
        if imagen_producto:
            return mark_safe(f'<img src="{imagen_producto.imagen.url}/>')  # Error en el cierre de la etiqueta
        return "Sin imagen"

    mostrar_imagen_producto.short_description = "Imagen del Producto"





class PedidoClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'nombre', 'apellido', 'celular', 'correo', 'direccion_envio', 'ciudad', 'codigo_postal', 'metodo_pago', 'estado', 'fecha_pedido')
    list_filter = ('estado', 'metodo_pago', 'ciudad', 'fecha_pedido')
    search_fields = ('nombre', 'apellido', 'correo', 'celular', 'ciudad')
    ordering = ('-fecha_pedido',)  # Mostrar los pedidos más recientes primero
    readonly_fields = ('fecha_pedido',)  # Campo de solo lectura

admin.site.register(PedidoCliente, PedidoClienteAdmin)


