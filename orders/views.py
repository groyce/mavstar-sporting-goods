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
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings 
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from .utils import render_to_pdf
#import weasyprint


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


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/order/detail.html',
                  {'order': order})
    

'''
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename= "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response

'''



@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(order.id, order.first_name)
    template = get_template('orders/order/pdf.html')  
    context = {
         'order':order
        }  
    html = template.render(context)
    pdf = render_to_pdf('orders/order/pdf.html',context)
    if pdf:
        response=  HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename= "order_{}.pdf"'.format(order.id)
        return response
    return HttpResponse("Not Found")












