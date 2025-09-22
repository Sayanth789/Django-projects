from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings 
from django.urls import reverse




class Contact(models.Model):
    user_form = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name = 'rel_to_set',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'    

# This(preceding) contais a contact model that will use for users r/s.
# user_from = A foreignKey for the user who crears the relationships
# user_to : foreignKey for the user being followed.
# created: A DateTimeField with auto_now_add=True to store the time when the relationships was created.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth= models.DateField(blank=True, null=True)
    photo  = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True
    )
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.user.username])
    



# Add the following field to User dynamically.

user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False
    )
    )    