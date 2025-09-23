from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from .fields import OrderField
from django.template.loader import render_to_string



class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )    

    subject = models.ForeignKey(
        Subject,
        related_name='course',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        User, 
        related_name='course_joined',
        blank=True
    )
    total_modules = models.IntegerField(default=0)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course =  models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])


    def __str__(self):
        return f'{self.order}. {self.title}'
    
    class Meta:
        ordering = ['order']



class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name = 'contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in':{'text', 'video', 'image', 'file'}
        },
    )

    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])


    # adding default ordering for both models.
    class Meta:
        ordering = ['order']

''' This is the Content model. A module contains multiple contents, so that we define a ForeignKey field that points to the Module model.'''


# Here we create an abstract base model that is extended by models - each designed to store a particular type of data:text, images, video and file.
# This flexible approach wil equip one with the tools needed for scenarios where polymorphism is required.

# This abstract model provides the common field for all content models

class ItemBase(models.Model):
    owner = models.ForeignKey(
        User, 
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    
    
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


    def __str__(self):
        return self.title
    
    def render(self):
        return render_to_string(
            f"course/content/{self._meta.model_name}.html",
            {"item": self},
        )

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')            
      
class Image(ItemBase):
    file = models.FileField(upload_to='images')
   
class Video(ItemBase):
    url = models.URLField()


# The subject, Course and Module models. The Course models are as follows:
# owner : The instructor who created the course
# subject : The subject that this course belongs to. It is a ForeignKey field that points to the subject model
# title : The title of the course
# slug : The slug of the course. This will be used in URL later
# overview : A TextField column to store an overview of the course.
# created : The date and time when the course was created.    


