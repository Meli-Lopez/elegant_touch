from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, PerfilUsuarioForm, ContactoForm, SubcategoriaForm, GestionCategoriaForm, CategoriaForm, MarcaForm,ProveedorForm ,ProductoForm, ReseñaForm, InventarioForm,VentaForm
from django.contrib import messages
from .models import Contacto, PerfilUsuario, Categoria, Producto,  Subcategoria, GestionCategoria, Marca,Proveedor, Producto,  ImagenProducto, ListaDeseos,Reseña, Inventario,Venta, Pedido
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages

# Vistas públicas
def carrito(request):
    return render(request, 'carrito.html')


def contacto(request):
    return render(request, 'contacto.html')

def tips(request):
    return render(request, 'tips.html')

def tips_maquillaje_piel(request):
    return render(request,'tips_maquillaje_piel.html' )


def tips_maquillaje_ojos(request):
    return render(request, 'tips_maquillaje_ojos.html')  

def tips_maquillaje_cejas(resquest):
    return render(resquest, 'tips_maquillaje_cejas.html')

def tips_labios(resquest):
    return render(resquest, 'tips_labios.html') 
    

def tips_rubor_iluminador(resquest):
    return render(resquest, 'tips_rubor_iluminador.html') 

def tips_contorno(resquest):
    return render(resquest, 'tips_contorno.html')

def index(request):
    return render(request, 'index.html')


def lista_de_deseos(request):
    return render(request, 'lista-de-deseos.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_active:
                auth_login(request, user)
                return redirect('index')
            else:
                # Mensaje de error si el usuario está inactivo
                messages.error(request, "Tu cuenta ha sido desactivada. Contacta al administrador para más información.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def my_account(request):
    return render(request, 'my-account.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = PerfilUsuarioForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            auth_login(request, user)
            return redirect('index')
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserRegistrationForm()
        profile_form = PerfilUsuarioForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def contacto(request):
    return render(request, 'contacto.html')

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos en la base de datos

            # Verifica si es una petición AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})  # Respuesta de éxito para AJAX
            else:
                return redirect('contacto_exitoso')  # Redirige a una página de éxito para peticiones normales
        else:
            # Si el formulario no es válido, responder dependiendo del tipo de petición
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Formulario inválido'})
            else:
                return render(request, 'contacto.html', {'form': form})  # Volver a renderizar con errores

    else:
        form = ContactoForm()

    return render(request, 'contacto.html',{'form':form})

@login_required
def user_info(request):
    perfil_usuario = PerfilUsuario.objects.get(user=request.user)

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('my_account')  # Redirige a la página de perfil después de guardar los cambios
    else:
        form = PerfilUsuarioForm(instance=perfil_usuario)

    return render(request, 'user_info.html', {
        'form': form,
        'user': request.user,
    })

def request_data(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Busca al usuario en la base de datos por su correo_cliente
        try:
            usuario = PerfilUsuario.objects.get(correo_cliente=email)
            # Prepara los datos del usuario para incluir en el correo
            user_data = f"""
            Nombre: {usuario.user.username}
            Dirección: {usuario.direccion}
            Teléfono: {usuario.telefono}
            """
            
            # Enviar el correo con los datos del usuario
            send_mail(
                'Solicitud de Datos Personales',
                f'Hola {usuario.user.username},\n\nAquí están tus datos personales:\n{user_data}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return HttpResponse('Solicitud recibida. Te enviaremos un correo con tus datos.')
        
        except PerfilUsuario.DoesNotExist:
            return HttpResponse('El correo electrónico proporcionado no está registrado.')
    
    return render(request, 'data_request.html')



@login_required
def index_admi(request):
    return render(request, 'index-admi.html')

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all().prefetch_related('subcategorias')
    return render(request, 'lista_categorias.html', {'categorias': categorias})


@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría agregada con éxito.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'agregar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada con éxito.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada con éxito.')
        return redirect('lista_categorias')
    return render(request, 'eliminar_categoria.html', {'categoria': categoria})

@login_required
def agregar_subcategoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            subcategoria = form.save(commit=False)
            subcategoria.categoria = categoria
            subcategoria.save()
            messages.success(request, 'Subcategoría agregada con éxito.')
            return redirect('lista_categorias')
    else:
        form = SubcategoriaForm(initial={'categoria': categoria})
    return render(request, 'agregar_subcategoria.html', {'form': form, 'categoria': categoria})

@login_required
def editar_subcategoria(request, pk):
    subcategoria = get_object_or_404(Subcategoria, pk=pk)
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategoría actualizada con éxito.')
            return redirect('lista_categorias')
    else:
        form = SubcategoriaForm(instance=subcategoria)
    return render(request, 'editar_subcategoria.html', {'form': form, 'subcategoria': subcategoria})

@login_required
def eliminar_subcategoria(request, pk):
    subcategoria = get_object_or_404(Subcategoria, pk=pk)
    if request.method == 'POST':
        subcategoria.delete()
        messages.success(request, 'Subcategoría eliminada con éxito.')
        return redirect('lista_categorias')
    return render(request, 'eliminar_subcategoria.html', {'subcategoria': subcategoria})

@login_required
def GestionCategoria(request):
    if request.method == 'POST':
        form = GestionCategoriaForm(request.POST)
        if form.is_valid():
            gestion = form.save(commit=False)
            gestion.usuario = request.user
            gestion.save()
            messages.success(request, 'Gestión de categoría registrada con éxito.')
            return redirect('lista_gestion_categorias')
    else:
        form = GestionCategoriaForm()
    return render(request, 'gestion_categoria.html', {'form': form})

@login_required
def lista_gestion_categorias(request):
    gestiones = GestionCategoria.objects.all().select_related('categoria', 'subcategoria', 'usuario')
    return render(request, 'lista_gestion_categorias.html', {'gestiones': gestiones})

@login_required
def crud_productos(request):
    productos = Producto.objects.all()
    return render(request, 'admin_crud-productos.html', {'productos': productos})

@login_required
def gestion_de_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'admin_gestion-de-pedidos.html')

@login_required
def gestion_de_usuarios(request):
    # Obtener los parámetros de búsqueda y filtro
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')

    # Filtrar los usuarios
    usuarios = PerfilUsuario.objects.all()

    # Aplicar búsqueda por nombre de usuario o correo electrónico
    if search_query:
        usuarios = usuarios.filter(
            Q(user__username__icontains=search_query) | 
            Q(correo_cliente__icontains=search_query)
        )

    # Aplicar filtro por rol si es necesario (ajusta según tu lógica)
    if role_filter:
        if role_filter == 'admin':
            usuarios = usuarios.filter(user__is_staff=True)
        elif role_filter == 'user':
            usuarios = usuarios.filter(user__is_staff=False)

    context = {
        'usuarios': usuarios,
        'search': search_query,
        'role': role_filter,
    }
    
    return render(request, 'admin_gestion_usuarios.html', context)  # Cambia 'tu_template.html' por el nombre de tu plantilla


@login_required
def editar_usuario(request, usuario_id):
    perfil_usuario = get_object_or_404(PerfilUsuario, id=usuario_id)
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado con éxito.')
            return redirect('gestion_de_usuarios')
    else:
        form = PerfilUsuarioForm(instance=perfil_usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'perfil_usuario': perfil_usuario})

@login_required
def toggle_user_status(request, user_id):
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=user_id)
    perfil_usuario.is_active = not perfil_usuario.is_active  # Cambia el estado en PerfilUsuario
    perfil_usuario.save()

    # Asegúrate de cambiar también el estado en el modelo User
    usuario = perfil_usuario.user  # Relación entre PerfilUsuario y User
    usuario.is_active = perfil_usuario.is_active
    usuario.save()

    if perfil_usuario.is_active:
        messages.success(request, "El usuario ha sido activado.")
    else:
        messages.warning(request, "El usuario ha sido inactivado.")
    return redirect('gestion_de_usuarios')



def dashboard_view(request):
    total_usuarios = PerfilUsuario.objects.count()
    usuarios_activos = PerfilUsuario.objects.filter(is_active=True).count()
    usuarios_inactivos = PerfilUsuario.objects.filter(is_active=False).count()
    usuarios_pendientes = PerfilUsuario.objects.filter(is_pending=True).count()

    # Depuración para revisar los valores antes de pasarlos al contexto
    print(f"Total Usuarios: {total_usuarios}")
    print(f"Usuarios Activos: {usuarios_activos}")
    print(f"Usuarios Inactivos: {usuarios_inactivos}")
    print(f"Usuarios Pendientes: {usuarios_pendientes}")

    # Pasar los valores al contexto
    return render(request, 'admin_gestion_usuarios.html', {
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'usuarios_inactivos': usuarios_inactivos,
        'usuarios_pendientes': usuarios_pendientes,
    })



@login_required
def verificar(request):
    # Lógica para la vista verificar
    return render(request, 'verificar.html')

def logout_user(request):
    logout(request)
    return redirect('login') 


#cambiar contraseña
class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset.html'
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Restablecer Contraseña'
        return context
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Correo Enviado'
        return context
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Restablecer Contraseña'
        return context
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contraseña Restablecida'
        return context
    

@login_required
def lista_marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'lista_marcas.html', {'marcas': marcas})

@login_required
def agregar_marca(request):
    if request.method == "POST":
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_marcas')  # Cambia esto por el nombre de tu URL
    else:
        form = MarcaForm()
    return render(request, 'agregar_marca.html', {'form': form})


@login_required
def editar_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    if request.method == "POST":
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            return redirect('lista_marcas')  # Cambia esto por el nombre de tu URL
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'editar_marca.html', {'form': form})


@login_required
def eliminar_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    if request.method == "POST":
        marca.delete()
        return redirect('lista_marcas')  # Cambia esto por el nombre de tu URL
    return render(request, 'eliminar_marca.html', {'marca': marca})

#Proveedores
#Listar Proveedores
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'lista_proveedores.html', {'proveedores': proveedores})


# Agregar Proveedor
def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form})

# Editar Proveedor
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form, 'proveedor': proveedor})

# Eliminar Proveedor
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('lista_proveedores')
    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})




#views productos

# Vista para listar los productos, incluyendo productos destacados y con búsqueda
def lista_productos(request):
    # Obtén el término de búsqueda de la URL
    query = request.GET.get('q', '')

    # Cargar todos los productos o filtrar por el término de búsqueda
    productos = Producto.objects.select_related('marca', 'categoria', 'subcategoria').all()
    
    # Filtrar productos si hay un término de búsqueda
    if query:
        productos = productos.filter(
            nombre_producto__icontains=query
        ) | productos.filter(
            categoria__nombre__icontains=query
        ) | productos.filter(
            subcategoria__nombre__icontains=query
        )

    # Renderiza la plantilla con la lista de productos (filtrada si hay una búsqueda)
    return render(request, 'admin_lista-productos.html', {
        'productos': productos,
    })


# Vista para eliminar un producto
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')  # Redirige a la lista de productos
    return render(request, 'producto_confirmar_eliminacion.html', {'producto': producto})

# Vista para agregar un nuevo producto
def producto_agregar(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # Incluye archivos para imágenes
        if form.is_valid():
            producto = form.save()  # Guarda el nuevo producto
            
            # Guarda las imágenes si se han subido
            if 'imagenes' in request.FILES:
                for img in request.FILES.getlist('imagenes'):
                    ImagenProducto.objects.create(producto=producto, imagen=img)
                    
            return redirect('lista_productos')  # Redirige a la lista de productos
    else:
        form = ProductoForm()  # Crea un formulario vacío

    return render(request, 'agregar_producto.html', {'form': form})

# Vista para editar un producto existente
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()

            # Manejo de las imágenes
            if 'imagenes' in request.FILES:
                for img in request.FILES.getlist('imagenes'):
                    ImagenProducto.objects.create(producto=producto, imagen=img)

            return redirect('lista_productos')  # Redirige a la lista de productos

    else:
        form = ProductoForm(instance=producto)

    return render(request, 'producto_editar.html', {'form': form, 'producto': producto})

# Vista para eliminar una imagen asociada a un producto
def imagen_eliminar(request, imagen_id):
    imagen = get_object_or_404(ImagenProducto, id=imagen_id)
    producto_id = imagen.producto.id  # Obtén el ID del producto asociado
    imagen.delete()
    return redirect('producto_editar', pk=producto_id)  # Redirigir usando pk

# Vista rápida de un producto
def vista_rapida(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'vista_rapida.html', {'producto': producto})





def index(request):
    # Filtra los productos nuevos
    productos_nuevos = Producto.objects.filter(es_nuevo=True)
    
    # Filtra los productos destacados
    productos_destacados = Producto.objects.filter(destacado=True)
    
    # Filtra los productos que no son ni destacados ni nuevos
    productos_regulares = Producto.objects.filter(es_nuevo=False, destacado=False)
    
    # Obtén todas las reseñas
    reseñas = Reseña.objects.all()

    # Pasar todos los datos necesarios al contexto
    return render(request, 'index.html', {
        'productos_nuevos': productos_nuevos,
        'productos_destacados': productos_destacados,
        'productos_regulares': productos_regulares,
        'reseñas': reseñas
    })



def productos_maquillaje_ojos(request):
    # Filtrar productos por categoría (ID 1) y subcategoría (ID 2)
    productos_ojos = Producto.objects.filter(categoria_id=1, subcategoria_id=2)
    
    return render(request, 'maquillaje-ojos.html', {
        'productos_ojos': productos_ojos,  # Asegúrate de pasar el nombre correcto
    })


def productos_maquillaje_rostro(request):
    # Filtrar productos por categoría (ID 1) y subcategoría (ID 2)
    productos_rostro = Producto.objects.filter(categoria_id=1, subcategoria_id=1)
    
    return render(request, 'maquillaje-rostro.html', {
        'productos_rostro': productos_rostro,  # Asegúrate de pasar el nombre correcto
    })


def productos_maquillaje_labios(request):
    # Filtrar productos por categoría (ID 1) y subcategoría (ID 2)
    productos_labios = Producto.objects.filter(categoria_id=1, subcategoria_id=3)
    
    return render(request, 'maquillaje-labios.html', {
        'productos_labios': productos_labios,  # Asegúrate de pasar el nombre correcto
    })



def productos_maquillaje_anti_envejecimiento(request):
    # Filtrar productos por categoría (ID 1) y subcategoría (ID 2)
    productos_anti_envejecimiento = Producto.objects.filter(categoria_id=1, subcategoria_id=4)
    
    return render(request, 'maquillaje-anti-envejecimiento.html', {
        'productos_anti_envejecimiento': productos_anti_envejecimiento,  # Asegúrate de pasar el nombre correcto
    })



def productos_maquillaje_waterproof(request):
    # Filtrar productos por categoría (ID 1) y subcategoría (ID 2)
    productos_maquillaje_waterproof = Producto.objects.filter(categoria_id=1, subcategoria_id=5)
    
    return render(request, 'maquillaje-waterproof.html', {
        'productos_maquillaje_waterproof': productos_maquillaje_waterproof,  # Asegúrate de pasar el nombre correcto
    })


def productos_limpiadores_faciales(request):
    
    productos_limpiadores_faciales = Producto.objects.filter(categoria_id=2, subcategoria_id=6)
    
    return render(request, 'limpiadores-faciales.html', {
        'productos_limpiadores_faciales': productos_limpiadores_faciales,  # Asegúrate de pasar el nombre correcto
    })


def productos_exfoliantes_hidratantes(request):
    
    productos_exfoliantes = Producto.objects.filter(categoria_id=2, subcategoria_id=7)
    
    return render(request, 'exfoliantes-hidratantes.html', {
        'productos_exfoliantes': productos_exfoliantes ,  # Asegúrate de pasar el nombre correcto
    })

def productos_serums_mascarillas(request):
    
    productos_serums_mascarillas = Producto.objects.filter(categoria_id=2, subcategoria_id=8)
    
    return render(request, 'serums-mascarillas.html', {
        'productos_serums_mascarillas': productos_serums_mascarillas,  # Asegúrate de pasar el nombre correcto
    })


def productos_protectores_cremas(request):
    
    productos_protectores_cremas = Producto.objects.filter(categoria_id=2, subcategoria_id=9)
    
    return render(request, 'protectores-cremas.html', {
        'productos_protectores_cremas': productos_protectores_cremas,  # Asegúrate de pasar el nombre correcto
    })


def productos_brochas_pinceles(request):
    
    productos_brochas_pinceles = Producto.objects.filter(categoria_id=3, subcategoria_id=10)
    
    return render(request, 'brochas-pinceles.html', {
        'productos_brochas_pinceles': productos_brochas_pinceles,  # Asegúrate de pasar el nombre correcto
    })

def productos_esponjas_aplicadores(request):
    
    productos_esponjas_aplicadores = Producto.objects.filter(categoria_id=3, subcategoria_id=11)
    
    return render(request, 'aplicadores.html', {
        'productos_esponjas_aplicadores': productos_esponjas_aplicadores,  # Asegúrate de pasar el nombre correcto
    })


def productos_otros_accesorios(request):
    
    productos_otros_accesorios = Producto.objects.filter(categoria_id=3, subcategoria_id=12)
    
    return render(request, 'otros-accesorios.html', {
        'productos_otros_accesorios': productos_otros_accesorios,  # Asegúrate de pasar el nombre correcto
    })



@login_required
def lista_de_deseos(request):
    lista_deseos = ListaDeseos.objects.filter(usuario=request.user)
    context = {
        'lista_deseos': lista_deseos,
    }
    return render(request, 'lista-de-deseos.html', context)


@login_required
def agregar_a_lista_deseos(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    ListaDeseos.objects.get_or_create(usuario=request.user, producto=producto)
    return redirect('lista_de_deseos')  # Redirige a la vista de lista de deseos


@login_required
def eliminar_de_lista_deseos(request, item_id):
    item = ListaDeseos.objects.get(id=item_id, usuario=request.user)
    item.delete()
    return redirect('lista_de_deseos')  # Redirige a la vista de lista de deseos

def contar_lista_deseos(request):
    if request.user.is_authenticated:
        conteo_lista_deseos = ListaDeseos.objects.filter(usuario=request.user).count()
    else:
        conteo_lista_deseos = 0  # Si el usuario no está autenticado
    return {'conteo_lista_deseos': conteo_lista_deseos}




def carrito(request):
    # Obtener el carrito de la sesión
    cart = request.session.get('cart', {})
    
    # Obtener detalles del producto en el carrito
    cart_items = []
    subtotal = 0
    
    for product_id, quantity in cart.items():
        try:
            producto = Producto.objects.get(id=product_id)
            item_total = producto.precio_producto * quantity
            subtotal += item_total
            
            cart_items.append({
                'product': producto,
                'quantity': quantity,
                'item_total': item_total,
            })
        except Producto.DoesNotExist:
            continue

    total = subtotal  # Añadir impuestos aquí si es necesario

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
    }
    return render(request, 'verificar.html', context)

@login_required(login_url='login')  # Redirige a la página de inicio de sesión si no está autenticado
def agregar_al_carrito(request, product_id):
    # Obtener los detalles del producto y la cantidad
    cantidad = int(request.POST.get('cantidad', 1))
    
    try:
        producto = Producto.objects.get(id=product_id)
        if cantidad > producto.stock_producto:
            # Si la cantidad supera el stock, agrega un mensaje de error al contexto
            context = {
                'error': f"La cantidad que seleccionaste supera las existencias actuales de este artículo. Quedan {producto.stock_producto} unidades.",
                'producto': producto,
                'mostrar_modal': True,  
            }
            return render(request, 'mensaje_stock.html', context)
        else:
            # Lógica para agregar el producto al carrito
            cart = request.session.get('cart', {})
            cart[product_id] = cantidad
            request.session['cart'] = cart
            return redirect('carrito')
    except Producto.DoesNotExist:
        # Manejar el caso donde el producto no existe
        return redirect('lista_productos')


def actualizar_carrito(request, product_id):
    # Obtener el carrito de la sesión
    cart = request.session.get('cart', {})
    
    # Obtener la cantidad del formulario
    nueva_cantidad = int(request.POST.get('cantidad', 1))
    
    if nueva_cantidad > 0:
        # Actualizar la cantidad en el carrito
        cart[product_id] = nueva_cantidad
    else:
        # Si la cantidad es 0, eliminar el producto del carrito
        cart.pop(product_id, None)
    
    # Guardar los cambios en la sesión
    request.session['cart'] = cart
    
    return redirect('verificar')  # Cambiar por la URL del carrito


def eliminar_producto(request, producto_id):
    # Obtener el carrito de la sesión
    cart = request.session.get('cart', {})
    
    # Verifica si el producto está en el carrito y lo elimina
    if str(producto_id) in cart:
        del cart[str(producto_id)]  # Eliminar el producto del carrito

    # Guardar el carrito actualizado en la sesión
    request.session['cart'] = cart

    # Redirigir de nuevo al carrito
    return redirect('verificar')


# Listar todas las reseñas de un producto
def listar_reseñas(request, producto_id):
    reseñas = Reseña.objects.filter(producto_id=producto_id)  # Filtra por producto_id
    return render(request, 'listar_reseñas.html', {'reseñas': reseñas})

# Ver reseñas de un producto
def ver_reseñas(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    reseñas = Reseña.objects.filter(producto=producto)
    return render(request, 'ver_reseñas.html', {'producto': producto, 'reseñas': reseñas})

# Escribir una nueva reseña
@login_required
def nueva_reseña(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            nueva_reseña = form.save(commit=False)
            nueva_reseña.producto = producto
            nueva_reseña.user = request.user  # Asocia la reseña con el usuario logueado
            nueva_reseña.save()
            return redirect('ver_reseñas', producto_id=producto.id)
    else:
        form = ReseñaForm()

    return render(request, 'nueva_reseña.html', {'form': form, 'producto': producto})

# Eliminar una reseña (solo si el usuario es el propietario)
@login_required
def eliminar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)

    # Verifica si el usuario actual es el propietario de la reseña
    if reseña.user != request.user:
        return render(request, '403.html', status=403)  # Redirige a una página de error 403

    if request.method == 'POST':
        producto_id = reseña.producto.id
        reseña.delete()
        return redirect('listar_reseñas', producto_id=producto_id)

    return render(request, 'eliminar_reseña.html', {'reseña': reseña})

def detalle_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)
    producto = reseña.producto  # Asegúrate de que la reseña tiene un atributo 'producto'
    return render(request, 'ver_reseñas.html', {'reseña': reseña, 'producto': producto})

# Editar una reseña (solo si el usuario es el propietario)
@login_required
def editar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)

    # Verifica si el usuario actual es el propietario de la reseña
    if reseña.user != request.user:
        return render(request, '403.html', status=403)  # Redirige a una página de error 403

    if request.method == 'POST':
        form = ReseñaForm(request.POST, instance=reseña)
        if form.is_valid():
            form.save()
            return redirect('detalle_reseña', reseña_id=reseña.id)
    else:
        form = ReseñaForm(instance=reseña)

    return render(request, 'editar_reseña.html', {'form': form, 'reseña': reseña})


def buscar_productos(request):
    # Recibe el término de búsqueda y la categoría seleccionada
    query = request.GET.get('query', '').strip()  # Elimina espacios al inicio y final
    categoria = request.GET.get('poscats', '').strip()  # Elimina espacios al inicio y final

    # Filtra todos los productos al inicio
    resultados = Producto.objects.all()

    # Filtra por nombre de producto si hay un término de búsqueda
    if query:
        resultados = resultados.filter(nombre_producto__icontains=query)

    # Filtra por categoría si se ha seleccionado una diferente de "Todas las categorias"
    if categoria and categoria != "Todas las categorias":
        resultados = resultados.filter(categoria__nombre=categoria)

        # Mapa de redirecciones basado en la categoría
        url_map = {
            "Maquillaje Ojos": 'maquillaje_ojos',
            "Maquillaje Rostro": 'maquillaje_rostro',
            "Maquillaje Labios": 'maquillaje_labios',
            "Maquillaje Anti Envejecimiento": 'maquillaje_anti_envejecimiento',
            "Maquillaje Waterproof": 'maquillaje_waterproof',
            "Limpiadores Faciales": 'limpiadores_faciales',
            "Exfoliantes e Hidratantes": 'exfoliantes_hidratantes',
            "Serums y Mascarillas": 'serums_mascarillas',
            "Protectores y Cremas": 'protectores_cremas',
            "Brochas y Pinceles": 'brochas_pinceles',
            "Aplicadores": 'aplicadores',
            "Otros Accesorios": 'otros_accesorios',
        }

        # Verifica si la categoría seleccionada está en el mapa y redirige
        if categoria in url_map:
            print(f"Redirigiendo a la URL de la categoría: {categoria}")
            return redirect(url_map[categoria])
        else:
            print(f"Categoría '{categoria}' no encontrada en el mapa de URLs")

    # Si no se selecciona una categoría específica, muestra resultados generales
    return render(request, 'resultados_busqueda.html', {'resultados': resultados, 'query': query})



#VIEWS INVENTARIO
def lista_inventario(request):
    query = request.GET.get('q')  # Obtener el parámetro de búsqueda de la URL
    if query:
        # Filtrar los inventarios cuyo nombre de producto contenga la palabra clave
        inventarios = Inventario.objects.filter(
            Q(producto__nombre_producto__icontains=query)
        )
    else:
        inventarios = Inventario.objects.select_related('producto').all()  # Obtener todos los inventarios si no hay búsqueda

    return render(request, 'lista_inventario.html', {'inventarios': inventarios, 'query': query})


def inventario_agregar(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            inventario = form.save()
            return redirect('lista_inventario')
    else:
        form = InventarioForm()
    return render(request, 'agregar_inventario.html', {'form': form})

def inventario_editar(request, pk):
    inventario = Inventario.objects.get(pk=pk)

    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            # Guardar el formulario y sincronizar con Producto
            form.save()
            return redirect('lista_inventario')  # Redirigir a la lista de inventarios
    else:
        form = InventarioForm(instance=inventario)

    return render(request, 'editar_inventario.html', {'form': form, 'inventario': inventario})


def inventario_eliminar(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete()
        return redirect('lista_inventario')
    return render(request, 'eliminar_inventario.html', {'inventario': inventario})



#VIEWS VENTAS
def lista_ventas(request):
    ventas = Venta.objects.all()  # Obtén todas las ventas de la base de datos
    return render(request, 'lista_ventas.html', {'ventas': ventas})


def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'detalle_venta.html', {'venta': venta})


def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ventas')  # Redirige a la lista de ventas después de crear
    else:
        form = VentaForm()
    
    return render(request, 'crear_venta.html', {'form': form})


def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('detalle_venta', venta_id=venta.id)  # Redirige al detalle de la venta
    else:
        form = VentaForm(instance=venta)
    
    return render(request, 'editar_venta.html', {'form': form, 'venta': venta})



def filtrar_ventas(request):
    estado = request.GET.get('estado', None)
    if estado:
        ventas = Venta.objects.filter(estado_venta=estado)
    else:
        ventas = Venta.objects.all()

    return render(request, 'filtrar_ventas.html', {'ventas': ventas})


def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.delete()
    return redirect('lista_ventas')


def ventas_por_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    ventas = Venta.objects.filter(cliente=cliente)
    return render(request, 'ventas_por_cliente.html', {'cliente': cliente, 'ventas': ventas})



#VIEWS PEDIDO
# Vista para listar todos los pedidos del cliente
@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_creacion')  # Filtramos por el cliente
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

# Vista para crear un nuevo pedido
@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = request.user  # Asociamos el pedido al usuario logueado
            pedido.save()
            return redirect('lista_pedidos')  # Redirigimos a la lista de pedidos
    else:
        form = PedidoForm()

    return render(request, 'crear_pedido.html', {'form': form})

# Vista para ver los detalles de un pedido específico
@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    return render(request, 'detalle_pedido.html', {'pedido': pedido})

# Vista para actualizar el estado de un pedido
@login_required
def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)

    if request.method == 'POST':
        # Si se desea actualizar el estado del pedido
        estado = request.POST.get('estado')
        if estado:
            pedido.estado = estado
            pedido.save()
            return redirect('detalle_pedido', pedido_id=pedido.id)

    return render(request, 'actualizar_pedido.html', {'pedido': pedido})

# Vista para cancelar un pedido
@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    if pedido.estado != 'cancelado':
        pedido.estado = 'cancelado'
        pedido.save()
        return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        return HttpResponse('Este pedido ya ha sido cancelado.')
    

@login_required
def historial_pedidos(request):
    # Obtiene los pedidos del usuario autenticado
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha_creacion')
    
    return render(request, 'historial_pedidos.html', {'pedidos': pedidos})
