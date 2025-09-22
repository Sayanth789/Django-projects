from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models
from  django.conf import settings



class Action(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='actions',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id'])

        ]
        ordering = ['-created']

# this shows Action model that'll be used to store user activities.
# The fields of this models are:
# user:  The user who performed the action, this is a ForeignKey to AUTH_USER_MODEL
# verb: The verb describing the action that the uesr has performed.
# created : The date and time when this action was created. We use auto_now_add=True to automatically set this to the current datetime when the object is saved for the first time in the DB.
