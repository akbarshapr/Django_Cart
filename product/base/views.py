from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from decimal import Decimal

from .models import Cart, Product

# Create your views here.


class ProductView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'index.html'


class CartView(ListView):
    model = Cart
    context_object_name = 'cart'
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_quantity = sum(item.quantity for item in cart_items)
        total_amount = sum(item.total_price for item in cart_items)

        offer_names = []

        discount_amount = Decimal(0)

        if total_quantity > 30 and any(item.quantity > 15 for item in cart_items):
            discount_amount = Decimal(
                0.5) * sum(item.item.price for item in cart_items if item.quantity > 15)
            offer_names.append("tiered_50_discount")
        elif total_quantity > 20:
            discount_amount = Decimal(0.1) * total_amount
            offer_names.append("bulk_10_discount")
        elif any(item.quantity > 10 for item in cart_items):
            discount_amount = Decimal(
                0.05) * sum(item.total_price for item in cart_items if item.quantity > 10)
            offer_names.append("bulk_5_discount")
        elif total_amount > 200:
            discount_amount = Decimal(10)
            offer_names.append("flat_10_discount")

        discounted_total_amount = total_amount - discount_amount
        context['total_amount'] = total_amount
        context['discounted_total_amount'] = discounted_total_amount.quantize(
            Decimal('0.00'))
        context['discount_amount'] = discount_amount.quantize(Decimal('0.00'))
        context['applied_offers'] = offer_names
        return context


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(item=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


def increase_quantity(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


def decrease_quantity(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    elif cart_item.quantity == 1:
        cart_item.delete()

    return redirect('cart')


def delete(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    cart_item.delete()

    return redirect('cart')
