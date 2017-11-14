from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Order
from sports.models import Category
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


@login_required
def order_create(request):
    categories = Category.objects.all()
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])  
            # clear the cart
            cart.clear()
            order_created(order.id)
            # launch asynchronous task
           # order_created.delay(order.id)
            #return render(request,'orders/order/created.html', {'order': order,'categories':categories})

            # launch asynchronous task
            #order_created.delay(order.id)  # set the order in the session
            request.session['order_id'] = order.id  # redirect to the payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,'orders/order/create.html', {'cart': cart, 'form': form,'categories':categories})



def order_created(order_id):
   #Task to send an e-mail notification when an order is successfully created.
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                  Your order id is {}.'.format(order.first_name,
                                            order.id)
    mail_sent = send_mail(subject,
                          message,
                          'mavstaruno@gmail.com',
                          [order.email]) #mavstaruno/@mavstar123
    return mail_sent