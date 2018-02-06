from django import forms
from django.db.models import Q
from .models import Project, User, Twitter_data, Dataset



class NewProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }

class GetDataForm(forms.Form):

    query = forms.CharField(label='Search query', max_length=100)
    number = forms.IntegerField(max_value=10000)
    result_choices = (('recent', 'Recent'),('mixed','Mixed'), ('popular', 'Popular'))
    result_type = forms.ChoiceField(choices=result_choices)