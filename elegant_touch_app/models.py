from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator
from decimal import Decimal

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    correo_cliente = models.EmailField(max_length=255, default='example@example.com')
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_pending = models.BooleanField(default=False) 
    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        # Asegurarte de que el correo electrónico del usuario se actualice cuando se actualice el correo_cliente
        self.user.email = self.correo_cliente
        self.user.save()
        super(PerfilUsuario, self).save(*args, **kwargs)


class Cliente(models.Model):
    perfil_usuario = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE)

    def _str_(self):
        return self.perfil_usuario.user.username
        


class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    apellido_proveedor = models.CharField(max_length=100)
    telefono_proveedor = models.CharField(max_length=20)
    correo_proveedor = models.EmailField()
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE, related_name='proveedores', null=True)

    def __str__(self):
        return f"{self.nombre_proveedor} {self.apellido_proveedor} - {self.marca.nombre_marca}"

        
class Marca(models.Model):
    nombre_marca = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre_marca

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, )

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"

class GestionCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Gestión de {self.categoria.nombre} - {self.subcategoria.nombre}"

    class Meta:
        verbose_name = "Gestión de Categoría"
        verbose_name_plural = "Gestiones de Categorías"



class MetodoDePago(models.Model):
    OPCIONES_METODO_PAGO = [
        ('Bancolombia', 'Bancolombia'),
        ('Nequi', 'Nequi'),
    ]

    nombre_metodo_pago = models.CharField(max_length=15, choices=OPCIONES_METODO_PAGO)

    def __str__(self):
        return self.nombre_metodo_pago





class Reseña(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=255, default="Sin título") 
    contenido = models.TextField(default="Sin contenido")  # Establece un valor por defecto
    calificacion = models.PositiveIntegerField(
        default=1, 
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # Validación de la calificación de 1 a 5
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Add blank=True and null=True if you want to allow nulls
    def __str__(self):
        return f"Reseña de {self.user.username} para {self.producto.nombre_producto}"


   
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    mensaje = models.TextField()

    def _str_(self):
        return self.nombre


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=50)
    descripcion_producto = models.TextField(max_length=1000)
    precio_producto = models.FloatField()
    stock_producto = models.IntegerField()
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    subcategoria = models.ForeignKey('Subcategoria', on_delete=models.CASCADE, related_name='productos', blank=True, null=True)
    es_nuevo = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)  # Permitir nulos

    def __str__(self):
        return self.nombre_producto


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/imagenes/')
    orden = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return f'Imagen de {self.producto.nombre_producto}'
    

class ListaDeseos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')  # Evita duplicados


class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name="inventario")
    descripcion = models.TextField()
    precio = models.FloatField()
    stock = models.IntegerField(default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='inventarios', blank=True, null=True)  # Hacer opcional
    cantidad_minima = models.IntegerField(default=10)
    cantidad_maxima = models.IntegerField(default=1000)
    entradas = models.IntegerField(default=0)
    salidas = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    ultima_entrada = models.DateTimeField(null=True, blank=True)
    ultima_salida = models.DateTimeField(null=True, blank=True)
    agotado = models.BooleanField(default=False)  # Si el producto está agotado o no

    def __str__(self):
        return f"Inventario de {self.producto.nombre_producto}"

        
    def actualizar_estado_agotado(self):
        """Método para actualizar el estado de agotado basado en el stock."""
        if self.stock <= 0:
            self.agotado = True
        else:
            self.agotado = False
        self.save()

    def actualizar_producto(self):
        """Método para actualizar los campos de Producto al guardar Inventario"""
        producto = self.producto
        producto.descripcion_producto = self.descripcion
        producto.precio_producto = self.precio
        producto.stock_producto = self.stock
        producto.save()

@receiver(post_save, sender=Inventario)
def sync_producto_on_inventario_save(sender, instance, created, **kwargs):
    """Sincroniza los cambios de Inventario en Producto"""
    if not created:  # Si no es una creación, es una actualización
        instance.actualizar_producto()

@receiver(post_delete, sender=Inventario)
def delete_producto_on_inventario_delete(sender, instance, **kwargs):
    """Elimina el Producto asociado cuando se elimina Inventario"""
    producto = instance.producto
    producto.delete()


class PedidoCliente(models.Model):
    METODO_PAGO_CHOICES = [
        ('bbva', 'BBVA'),
        ('nequi', 'Nequi'),
    ]
    
    ESTADO_PEDIDO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    cliente = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='pedidos', null=True, blank=True)
    nombre = models.CharField("Nombre", max_length=100)
    apellido = models.CharField("Apellido", max_length=100)
    celular_validator = RegexValidator(regex=r'^\d{10}$', message="El número de celular debe tener 10 dígitos y solo contener números.")
    celular = models.CharField("Celular", max_length=15, validators=[celular_validator], default=1)
    correo = models.EmailField("Correo electrónico", max_length=254, default=None)
    direccion_envio = models.CharField("Dirección de envío", max_length=255)
    ciudad = models.CharField("Ciudad", max_length=100)
    codigo_postal = models.CharField("Código postal", max_length=5)
    metodo_pago = models.CharField("Método de pago", max_length=20, choices=METODO_PAGO_CHOICES)
    comprobante_pago = models.FileField("Comprobante de pago", upload_to='comprobantes/', null=True, blank=True)
    estado = models.CharField("Estado del pedido", max_length=10, choices=ESTADO_PEDIDO_CHOICES, default='pendiente')
    fecha_pedido = models.DateTimeField("Fecha del pedido", auto_now_add=True)
    total = models.DecimalField("Total del pedido", max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = "Pedido de cliente"
        verbose_name_plural = "Pedidos de clientes"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido de {self.nombre} {self.apellido} - {self.fecha_pedido.strftime('%d/%m/%Y')} - {self.estado}"

    def get_total_items(self):
        return sum(detalle.cantidad for detalle in self.detalles.all())

    def actualizar_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(PedidoCliente, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.cantidad}"
