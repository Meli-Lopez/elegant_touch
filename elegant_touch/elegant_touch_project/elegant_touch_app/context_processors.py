from .models import ListaDeseos  # Asegúrate de que esta línea esté aquí
from .models import Producto

def contar_lista_deseos(request):
    if request.user.is_authenticated:
        conteo_lista_deseos = ListaDeseos.objects.filter(usuario=request.user).count()
    else:
        conteo_lista_deseos = 0  # Si el usuario no está autenticado
    return {'conteo_lista_deseos': conteo_lista_deseos}

def example_context_processor(request):
    return {
        'example_variable': 'Este es un ejemplo de contexto',
    }


def carrito_context(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            producto = Producto.objects.get(id=product_id)
            item_total = producto.precio_producto * quantity
            total += item_total
            
            cart_items.append({
                'product': producto,
                'quantity': quantity,
                'item_total': item_total,
            })
        except Producto.DoesNotExist:
            continue

    return {
        'cart_items': cart_items,
        'cart_total': total,
    }

