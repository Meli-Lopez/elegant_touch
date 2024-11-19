from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    # Rutas de la tienda
    path('', views.index, name='index'),
    path('carrito/', views.carrito, name='carrito'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('tips/', views.tips, name='tips'),
    path('lista-de-deseos/', views.lista_de_deseos, name='lista_de_deseos'),
    path('my-account/', views.my_account, name='my_account'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('verificar/', views.verificar, name='verificar'),
    path('informacion/', views.user_info, name='informacion'),

    # Rutas de autenticación
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Cambia `login_user` por `login_view` si ese es el nombre correcto
    path('logout/', views.logout_user, name='logout'),

    # Rutas adicionales
    path('solicitar-datos/', views.request_data, name='request_data'),
    path('data-request/', views.request_data, name='data_request'),

    # Rutas de administración
     path('index_admi/', views.index_admi, name='index_admi'),
     path('categorias/', views.lista_categorias, name='lista_categorias'),
     path('categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
     path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
     path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
     path('tips_maquillaje_piel/', views.tips_maquillaje_piel, name='tips_maquillaje_piel'),
     path('tips_maquillaje_ojos/', views.tips_maquillaje_ojos, name='tips_maquillaje_ojos'),
     path('tips_maquillaje_cejas/', views.tips_maquillaje_cejas, name='tips_maquillaje_cejas'),
     path('tips_labios/', views.tips_labios, name='tips_labios'),
     path('tips_rubor_iluminador/', views.tips_rubor_iluminador, name='tips_rubor_iluminador'),
     path('tips_contorno/', views.tips_contorno, name='tips_contorno'),
     path('categorias/<int:categoria_id>/agregar-subcategoria/', views.agregar_subcategoria, name='agregar_subcategoria'),
     path('subcategorias/editar/<int:pk>/', views.editar_subcategoria, name='editar_subcategoria'),
     path('subcategorias/eliminar/<int:pk>/', views.eliminar_subcategoria, name='eliminar_subcategoria'),
     path('gestion-categorias/', views.GestionCategoria, name='GestionCategoria'),
     path('gestion-categorias/lista/', views.lista_gestion_categorias, name='lista_gestion_categorias'),
     path('marcas/', views.lista_marcas, name='lista_marcas'),
     path('marcas/agregar/', views.agregar_marca, name='agregar_marca'),
     path('marcas/editar/<int:marca_id>/', views.editar_marca, name='editar_marca'),
     path('marcas/eliminar/<int:marca_id>/', views.eliminar_marca, name='eliminar_marca'),
     path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
     path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
     path('proveedores/editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
     path('proveedores/eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
     path('gestion-de-usuarios/', views.gestion_de_usuarios, name='gestion_de_usuarios'),
     path('editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
     path('toggle-user-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
     path('dashboard/', views.dashboard_view, name='dashboard'),
     path('productos/', views.lista_productos, name='lista_productos'),
     path('producto/agregar/', views.producto_agregar, name='producto_agregar'),
     path('producto/editar/<int:pk>/', views.producto_editar, name='producto_editar'),
     path('imagen/eliminar/<int:imagen_id>/', views.imagen_eliminar, name='imagen_eliminar'), # Esta es la ruta que necesitas
     path('producto/eliminar/<int:pk>/', views.producto_eliminar, name='producto_eliminar'),
     path('producto/vista-rapida/<int:producto_id>/', views.vista_rapida, name='vista_rapida'),
     path('maquillaje-ojos/', views.productos_maquillaje_ojos, name='maquillaje_ojos'),
     path('maquillaje-rostro/', views.productos_maquillaje_rostro, name='maquillaje_rostro'),
     path('maquillaje-labios/', views.productos_maquillaje_labios, name='maquillaje_labios'),
     path('maquillaje_anti_envejecimiento/', views.productos_maquillaje_anti_envejecimiento, name='maquillaje_anti_envejecimiento'),
     path('maquillaje_waterproof/', views.productos_maquillaje_waterproof, name='maquillaje_waterproof'),
     path('limpiadores-faciales/', views.productos_limpiadores_faciales, name='limpiadores_faciales'),
     path('exfoliantes-hidratantes/', views.productos_exfoliantes_hidratantes, name='exfoliantes_hidratantes'),
     path('serums-mascarillas/', views.productos_serums_mascarillas, name='serums_mascarillas'),
     path('protectores-cremas/', views.productos_protectores_cremas, name='protectores_cremas'),
     path('brochas-pincles/', views.productos_brochas_pinceles, name='brochas_pinceles'),
     path('aplicadores/', views.productos_esponjas_aplicadores, name='aplicadores'),
     path('otros-accesorios/', views.productos_otros_accesorios, name='otros_accesorios'),
     path('lista-de-deseos/', views.lista_de_deseos, name='lista_de_deseos'),
     path('agregar-a-lista-deseos/<int:producto_id>/', views.agregar_a_lista_deseos, name='agregar_a_lista_deseos'),
     path('eliminar-de-lista-deseos/<int:item_id>/', views.eliminar_de_lista_deseos, name='eliminar_de_lista_deseos'),
     path('agregar-al-carrito/<int:product_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
     path('carrito/', views.carrito, name='verificar'),
     path('carrito/actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
     path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
     path('reseñas/listar//<int:producto_id>/', views.listar_reseñas, name='listar_reseñas'),
     path('reseñas/<int:producto_id>/', views.ver_reseñas, name='ver_reseñas'),
     path('reseña/nueva/<int:producto_id>/', views.nueva_reseña, name='nueva_reseña'),
     path('reseña/eliminar/<int:reseña_id>/', views.eliminar_reseña, name='eliminar_reseña'),
     path('reseña/<int:reseña_id>/', views.detalle_reseña, name='detalle_reseña'),
     path('reseña/editar/<int:reseña_id>/', views.editar_reseña, name='editar_reseña'),
     path('buscar/', views.buscar_productos, name='buscar_productos'),
     path('inventario/', views.lista_inventario, name='lista_inventario'),
     path('inventario/agregar/', views.inventario_agregar, name='inventario_agregar'),
     path('inventario/editar/<int:pk>/', views.inventario_editar, name='inventario_editar'),
     path('inventario/eliminar/<int:pk>/', views.inventario_eliminar, name='inventario_eliminar'),
     path('ventas/', views.lista_ventas, name='lista_ventas'),
     path('ventas/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),  # Detalle de una venta
     path('ventas/crear/', views.crear_venta, name='crear_venta'),  # Crear una nueva venta
     path('ventas/<int:venta_id>/editar/', views.editar_venta, name='editar_venta'),  # Editar una venta
     path('ventas/filtrar/', views.filtrar_ventas, name='filtrar_ventas'),  # Filtrar ventas por estado
     path('ventas/<int:venta_id>/eliminar/', views.eliminar_venta, name='eliminar_venta'),  # Eliminar una venta
     path('clientes/<int:cliente_id>/ventas/', views.ventas_por_cliente, name='ventas_por_cliente'),  # Ventas por cliente
     path('pedidos/', views.lista_pedidos, name='lista_pedidos'),  # Lista de pedidos
     path('pedido/crear/', views.crear_pedido, name='crear_pedido'),  # Crear nuevo pedido
     path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),  # Ver detalles de un pedido
     path('pedido/<int:pedido_id>/actualizar/', views.actualizar_pedido, name='actualizar_pedido'),  # Actualizar estado de pedido
     path('pedido/<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),  # Cancelar un pedido
     path('historial_pedidos/', views.historial_pedidos, name='historial_pedidos'),
     
    #Ruta cambio de contraseña(si se le olvido)
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='reset_password'),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
