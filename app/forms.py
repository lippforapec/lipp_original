from django import forms
from jsonfield import JSONField
from .models import Startup

class SimpleStartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = ('name', 'location', 'raiseAmount', 'product_name', 'category', 'tags', 'summary')
        # 'background','market', 'solution', 'business_model', 'future', 'raiseAmount',
        # 'timeline', 'location', 'summary', 'members', 'team_desc')

class StartupForm(forms.Form):
    name = forms.CharField(
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter the name of your company or team'
            }
        ),
        help_text=''
    )

    location = forms.CharField(
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter the base location of your company or team'
            }
        ),
        help_text = ''
    )

    raiseAmount = forms.CharField(
        label = 'Raise amount',
        widget = forms.NumberInput(
            attrs = {
                'placeholder': 'Enter the amount you want to raise'
            }
        ),
        help_text = 'This will be shown in the detail page of your project.'
    )

    tags = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                'id': 'tags',
                'data-role': 'tagsinput',
                'value': 'startup,'
            }
        ),
        help_text = 'Written tags will be used to crawl relative articles for the information and help you to writing a better portfolio.'
    )

    product_name = forms.CharField(
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter the name of your company or team'
            }
        ),
        help_text = 'This will be shown on the first page. Please write your project name attractively so that VCs want to click.'
    )

    CATEGORIES = (('1', 'Technology'),('2', 'Bio'),)
    category = forms.ChoiceField(
        choices=CATEGORIES,
        help_text='This will decide where your project is shown.'
    )

    summary = forms.CharField(
        max_length = 500,
        widget = forms.Textarea(
            attrs = {
                'rows': 3
            }
        ),
        help_text = 'This will be shown on the first page. Please write your project name attractively so that VCs want to click.'
    )

    cover_photo = forms.FileField()
