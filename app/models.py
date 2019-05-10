from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

# validators
from app.validators import validate_timeline, validate_members
# for saving timelines
import operator
import json
# import category constants 
import app.categories as cate







# Like Models
class Like(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# Startup Models
class Startup(models.Model):
    user = models.ForeignKey('auth.User', related_name = "startups", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default="",max_length=50)
    product_name = models.CharField(default="",max_length=50)
    state = models.PositiveSmallIntegerField(default=0)
    category = models.PositiveSmallIntegerField(choices=cate.CATEGORIES,default=0)
    tags = ArrayField(models.CharField(max_length=100),blank=True,null=True)
    background = models.TextField(default="")
    market = models.TextField(default="")
    solution = models.TextField(default="")
    business_model = models.TextField(default="")
    future = models.TextField(default="")
    raiseAmount = models.PositiveIntegerField(default=0)
    timeline = JSONField(default=dict,validators=[validate_timeline])
    location = models.CharField(default="",max_length=50)
    summary = models.CharField(default="",max_length=255)
    members = JSONField(default=dict,validators=[validate_members])
    team_desc = models.TextField(default="")
    def save(self, *args, **kwargs):
        timeline_unordered = [dict(data) for data in self.timeline]
        timeline_ordered = sorted(timeline_unordered, key=operator.itemgetter('date')) 
        self.timeline = timeline_ordered
        super(Startup, self).save(*args, **kwargs)

# Feedback Models
class Feedback(models.Model):
    user = models.ForeignKey('auth.User', related_name = "feedbacks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback =  models.TextField()
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE, default=0)
    reply = models.TextField()


# Article Models
class Article(models.Model):
    created_at =  models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    link = models.URLField()
    tags = ArrayField(models.CharField(max_length=100),blank=True,null=True)
    category = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ('created_at',)

# Google Results Models
class Search(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    results = JSONField(default=dict)
    query = models.CharField(max_length=100,default="")
    category = models.PositiveSmallIntegerField(null=True)
    topic = models.CharField(max_length=50)
    tags = ArrayField(models.CharField(max_length=100),blank=True,null=True)
    published_at = models.DateTimeField(null=True)
    #title = models.CharField(max_length=200)
    #link = models.URLField()
    #summary = models.TextField()
    
    #rank = models.PositiveIntegerField()

    
    