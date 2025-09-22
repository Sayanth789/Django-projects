from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text = 'Percentage value(0 to 100)'

    )
    active = models.BooleanField()

    def __str__(self):
        return self.code 


# Here,
#  code : The 'code' user have to enter inorder to apply the coupon to their purchase.
#  valid_from : The datetime value that indicates when the coupon becomes valid.
# valid_to : The datetime value that indicates when the coupon becomes invalid.
# discount : The discount rate to apply ( that is percentage, so it takes values 0 to 100).
# active: A Boolean that indicate whether the coupon is active.
