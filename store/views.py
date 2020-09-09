from django.shortcuts import render, redirect, HttpResponse
from .models import *
import random
# Create your views here.


def store(request):
    data = {
        "title": "Store",
        "products": Product.objects.all()
    }
    return render(request, 'store.html', data)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False
        )
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}

    data = {
        "items": items,
        "order": order,
        "title": "Cart"
    }
    return render(request, 'cart.html', data)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()

        addressCustomer = ShippingAddress.objects.get(customer=customer)
        if addressCustomer:
            data = {
                "items": items,
                "order": order,
                "addressCustomer": addressCustomer,
                "title": "Checkout"
            }
            print(addressCustomer.state)
            return render(request, 'checkout.html', data)
        else:
            if request.POST:
                customer = request.user.customer
                order = Order.objects.get(customer=customer)
                address = request.POST['address']
                city = request.POST['city']
                state = request.POST['state']
                zipCode = request.POST['zip-code']

                shippingAddress, created = ShippingAddress.objects.get_or_create(
                    customer=customer,
                    order=order,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipCode
                )
                addressCustomer = ShippingAddress.objects.get(
                    customer=customer)
                if created:
                    Order.objects.update(
                        customer=customer, complete=True, transaction_id=random.randint(2, 999999999))
                    return redirect('store')
                else:
                    return HttpResponse("Data Gagal Ditambahkan")
            data = {
                "items": items,
                "order": order,
                # "addressCustomer": addressCustomer,
                "title": "Checkout"
            }
            return render(request, 'checkout.html', data)

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0}

    data = {
        "items": items,
        "order": order,
        # "addressCustomer": addressCustomer,
        "title": "Checkout"
    }
    return render(request, 'checkout.html', data)


def view_item(request, id):
    product = Product.objects.get(id=id)
    if request.POST:
        customer = request.user.customer
        quantity = int(request.POST["qty"])
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(
            quantity=quantity, product=product, order=order)
        return redirect('cart')
    else:
        data = {
            "title": f"Detail {product.name}",
            "product": product
        }
        return render(request, 'detail_item.html', data)


def delete_cart(request, id):
    item = OrderItem.objects.get(id=id)
    item.delete()
    return redirect('cart')
