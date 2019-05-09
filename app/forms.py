from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Startup

class StartupForm(forms.ModelForm):
# help text 
    # name : string 50자 넘기지 말아야 
    # product_name 
    # cateogry : only in enum
    # tags : string list 
    # background ~ future : text 
    # raseAmount : int but over zero 
    # timeline : json of timeline , .... using JSON parser 
    # location : String 이지만 later 
    # summary : short text 
    # members : json 
    # team_desc : short text 
    class Meta:
        model = Startup
        fields = ('name', 'product_name', 'category', 'tags', 'background',
        'market', 'solution', 'business_model', 'future', 'raiseAmount',
        'timeline', 'location', 'summary', 'members', 'team_desc')
        help_texts = {'name':_("Write down your team name")}

        