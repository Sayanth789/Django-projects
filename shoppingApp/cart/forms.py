from django import forms
from django.utils.translation import gettext_lazy as _


PRODUCT_QUALITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUALITY_CHOICES,
        coerce=int,
        label=("Quantity")
    )
    # this field allow user to select a quantity b/w 1 and 20. TypedChoiceField with coerce=True convert the in: to an int.

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
        
    )