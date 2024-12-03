from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Contacto, Subcategoria, Categoria, GestionCategoria,Marca, Proveedor, Producto, ImagenProducto, Reseña, Inventario,PedidoCliente
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



class PedidoClienteForm(forms.ModelForm):
    class Meta:
        model = PedidoCliente
        fields = [
            'nombre', 
            'apellido', 
            'celular',
            'correo',
            'direccion_envio', 
            'ciudad', 
            'codigo_postal', 
            'metodo_pago', 
            'comprobante_pago', 
            
        ]
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'comprobante_pago': forms.FileInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'})  # Widget para el correo
        }

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular:
            raise forms.ValidationError("Este campo es obligatorio.")
        return celular

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        # Puedes agregar más validaciones si es necesario (por ejemplo, verificar si es un correo válido)
        return correo
    # Validación para el campo comprobante_pago para asegurar que sea una imagen
    def clean_comprobante_pago(self):
        comprobante = self.cleaned_data.get('comprobante_pago')
        if comprobante:
            # Comprobar que el archivo sea una imagen
            if not comprobante.name.endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("El comprobante de pago debe ser una imagen (JPG, JPEG, PNG).")
        return comprobante
    
