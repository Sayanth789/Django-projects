from django import forms 

from courses.models import Course

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
            queryset=Course.objects.none(),
            widget=forms.HiddenInput
        
    )

    def __init__(self, *args, **kwargs):
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        # above line calls the original __init__ method of forms.Form
        self.fields['course'].queryset = Course.objects.all()

