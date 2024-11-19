from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Contacto, Subcategoria, Categoria, GestionCategoria,Marca, Proveedor, Producto, ImagenProducto, Reseña, Inventario, Venta, Pedido
 # O la ruta correcta de importación


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Contraseña'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar Contraseña'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
        

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['correo_cliente', 'direccion', 'telefono']
        

        

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'telefono', 'direccion', 'mensaje']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'categoria']

class GestionCategoriaForm(forms.ModelForm):
    class Meta:
        model = GestionCategoria
        fields = ['categoria', 'subcategoria']


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre_marca']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor', 'apellido_proveedor', 'telefono_proveedor', 'correo_proveedor', 'marca']




class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre_producto',
            'descripcion_producto',
            'precio_producto',
            'stock_producto',
            'marca',
            'categoria',
            'subcategoria',
            'es_nuevo',
            'destacado',
        ]



class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['titulo', 'contenido', 'calificacion']  # Asegúrate de incluir solo los campos que quieres que el usuario complete



class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'precio', 'stock', 'proveedor', 'cantidad_minima', 'cantidad_maxima', 'agotado']



class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta  # Modelo al que se asocia el formulario
        fields = [
            'guia_pedido',
            'fecha_venta',
            'total_venta',
            'estado_venta',
            'cliente',
            'metodo_de_pago',
        ]
        widgets = {
            'fecha_venta': forms.DateInput(attrs={'type': 'date'}),  # Selector de fecha
            'total_venta': forms.NumberInput(attrs={'step': '0.01'}),  # Input numérico con paso decimal
            'estado_venta': forms.Select(choices=Venta.OPCIONES_ESTADO_VENTA),  # Selector de opciones
        }


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'estado', 'total', 'direccion_envio', 'detalles_adicionales']  # Incluye el campo 'cliente'

        # Personaliza los campos del formulario
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),  # Selector para elegir el cliente
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total del pedido'}),
            'direccion_envio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Escribe la dirección de envío'}),
            'detalles_adicionales': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Detalles adicionales del pedido'}),
        }
        labels = {
            'cliente': 'Cliente',
            'estado': 'Estado del Pedido',
            'total': 'Total',
            'direccion_envio': 'Dirección de Envío',
            'detalles_adicionales': 'Detalles Adicionales',
        }