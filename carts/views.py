from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):  # _cart_id  front _ declare it is private functions.
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart



def add_cart(request, product_id):
	color = request.GET['color']
	size = request.GET['size']
	product = Product.objects.get(id=product_id)  #get the product

	try:
		cart = Cart.objects.get(cart_id=_cart_id(request)) #get teh cart using the cart_id present in the sessions
	except Cart.DoesNotExist:
		cart = Cart.objects.create(cart_id = _cart_id(request))
		cart.save()

	try:
		cart_item = CartItem.objects.get(product=product, cart=cart)
		cart_item.quantity +=1
		cart_item.save()
	except CartItem.DoesNotExist:
		cart_item= CartItem.objects.create(product=product, quantity=1, cart=cart)
		cart_item.save()
	return redirect('carts')


def remove_cart(request, product_id):
	cart=Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item= CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity>1:
		cart_item.quantity -=1
		cart_item.save()
	else:
		cart_item.delete()

	return redirect('carts')



def carts(request, total=0, quantity=0, cart_item=None):
	try:
		tax=0
		grand_total=0
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, is_active=True)
		for cart_item in cart_items:
			total+=(cart_item.product.price * cart_item.quantity)
			quantity += cart_item.quantity

		tax = (2 * total)/100
		grand_total = total + tax
	except ObjectDoesNotExist:
		pass


	return render(request, 'carts.html', {'total':total, 'quantity':quantity, 'cart_items':cart_items, 'tax':tax, 'grand_total':grand_total})