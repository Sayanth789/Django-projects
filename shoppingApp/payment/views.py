from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

# THIS is the code for generating a PDF invoice for existing orders using the administration site.
import weasyprint
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']= f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))]
)
    return response

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id')
    order  = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        ) 
        cancel_url = request.build_absolute_uri(
            reverse('payment:cancelled')
        )
        # stripe checkout session data.
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # add order items to stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price-data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currecny':'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )

            # stripe coupon

        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duartion='once'
            )
            session_data['discounts'] = [{'coupon': stripe_coupon.id}]

        # create stripe checkout session.
        session = stripe.checkout.session.create(**session_data)
        # redirect to stripe payment form 
        return redirect(session.url, code=303)
    
    else:
        return render(request, 'payment/process.html', locals())

def payment_complete(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

