from shop.models import Product
from shop.recommender import Recommender
import stripe 
from django.conf import settings 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed


@csrf_exempt 
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try: 
        event = stripe.Webhook.contruct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid patload 
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # invalid singnature.
        return HttpResponse(status=400)
    
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if (
            session.mode == 'payment'
            and session.payment_status == 'paid' 
        ):
            try: 
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            # Mark order as paid 
            order.paid = True
            # store Stripe payment ID.
            order.stripe_id = session.payment_intent
            order.save()

            # save itenms bought for product recommendations
            product_ids = order.items.values_list('product_id')
            products = Product.objects.filter(id__in=product_ids)
            r = Recommender()
            r.products_bought(products)
            
            # With this change when receiving a webhook notification for a completed checkout session, the 
            # payment intent ID is stored in the stripe_id field of Order object.

            # Launch asynchronous task 
            payment_completed.delay(order.id)

                
    
    return HttpResponse(status=200)





