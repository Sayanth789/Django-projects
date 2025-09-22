from django.utils.translation import gettext_lazy as _
from django.urls import path
from .  import views, webhooks

app_name = 'payment'

urlpatterns = [
    path(_('process/'), views.payment_process, name='process'),
    path(_('completed/'), views.payment_complete, name='completed'),
    path(_('cancelled/'), views.payment_canceled, name='cancelled'),
  
    
]