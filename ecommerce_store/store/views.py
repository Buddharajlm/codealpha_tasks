from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal

from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm, RegisterForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_products': products.count(),
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    override = request.POST.get('override', 'false').lower() == 'true'

    if not product.in_stock:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Product is out of stock.'}, status=400)
        messages.error(request, f'"{product.name}" is currently out of stock.')
        return redirect('store:cart_detail')

    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, f'Added "{product.name}" to your cart.')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'"{product.name}" added to cart.',
            'total_items': len(cart),
            'subtotal': str(cart.get_subtotal_price()),
            'shipping': str(cart.get_shipping_cost()),
            'total': str(cart.get_total_price()),
        })

    return redirect(request.POST.get('next', 'store:cart_detail'))


def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        cart.remove(product)
        messages.info(request, f'Removed "{product.name}" from cart.')
    else:
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, f'Updated quantity for "{product.name}".')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_items': len(cart),
            'subtotal': str(cart.get_subtotal_price()),
            'shipping': str(cart.get_shipping_cost()),
            'total': str(cart.get_total_price()),
        })

    return redirect('store:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'Removed "{product.name}" from your cart.')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_items': len(cart),
            'subtotal': str(cart.get_subtotal_price()),
            'shipping': str(cart.get_shipping_cost()),
            'total': str(cart.get_total_price()),
        })

    return redirect('store:cart_detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add products before checking out.")
        return redirect('store:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Validate stock availability
            for item in cart:
                prod = item['product']
                if prod.stock < item['quantity']:
                    messages.error(request, f'Not enough stock for "{prod.name}". Only {prod.stock} available.')
                    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})

            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            order.subtotal = cart.get_subtotal_price()
            order.shipping_cost = cart.get_shipping_cost()
            order.total_amount = cart.get_total_price()
            order.save()

            # Create OrderItems and decrement product inventory
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=item['price'],
                    quantity=item['quantity']
                )
                product.stock -= item['quantity']
                if product.stock <= 0:
                    product.stock = 0
                product.save()

            # Clear session cart
            cart.clear()
            messages.success(request, f"Order #{order.order_number} has been placed successfully!")
            return redirect('store:order_confirmation', order_number=order.order_number)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to ShopZone, {user.username}! Your account has been created.")
            return redirect('store:product_list')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:product_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'store:product_list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('store:product_list')
