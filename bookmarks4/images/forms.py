import  requests  # this is an installed 3rd party lib.
from django.core.files.base import ContentFile
from django.utils.text import slugify 
from django import forms
from images.models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput(),
        }

        # This is for Cleaning form fields.
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not match valid images extensions.'
            )
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # Download the image from the given URL.
        response = requests.get(image_url)
        image.image.save(
            image_name, 
            ContentFile(response.content),
            save=False
        ) 
        if commit:
            image.save()
        return image    
# this is for getting particular type of images ending with jpeg, jpg, and png..etc
