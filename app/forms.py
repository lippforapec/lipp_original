from django import forms

from .models import Startup

class StartupForm(forms.ModelForm):

    class Meta:
        model = Startup
        fields = ('name', 'product_name', 'category', 'tags', 'background',
        'market', 'solution', 'business_model', 'future', 'raiseAmount',
        'timeline', 'location', 'summary', 'members', 'team_desc')
