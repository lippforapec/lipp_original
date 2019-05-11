from django.contrib import admin
from .models import Like, Startup, Feedback, Search
# Register your models here.
admin.site.register(Startup)
admin.site.register(Like)
admin.site.register(Search)
admin.site.register(Feedback)