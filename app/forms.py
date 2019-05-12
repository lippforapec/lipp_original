from django import forms
from jsonfield import JSONField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Startup, Like
import app.categories as cate
# accounts 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

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

    category = forms.ChoiceField(
        choices = cate.CATEGORIES,
        help_text = 'This will decide where your project is shown.'
    )

    summary = forms.CharField(
        max_length = 500,
        widget = forms.Textarea(
            attrs = {
                'rows': 3,
                'placeholder': 'Write what you do and build briefly.'
            }
        ),
        help_text = 'This will be shown on the first page. Please write your project name attractively so that VCs want to click.'
    )

    cover_photo = forms.FileField()


## 
class LikeForm(forms.Form):
    user_id = forms.IntegerField()
    startup_id = forms.IntegerField()
    def save(self, commit=True):
        like = Like.objects.create(
            user_id = self.cleaned_data['user_id'],
            startup_id = self.cleaned_data['startup_id'],
        )
        return like

## accounts 


 
 
class CustomUserCreationForm(forms.Form):
    first_name = forms.CharField(label='Enter your firstname',max_length=150)
    last_name = forms.CharField(label='Enter your lastname',max_length=150)
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter your email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput,min_length=8)
    password2 = forms.CharField(label='Confirm password again', widget=forms.PasswordInput,min_length=8)
 
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].title()
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")

        if len(password1) < 8:
            raise ValidationError('Password too short')
        return password1
 
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['first_name'],
        )
        return user