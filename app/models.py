from django.db import models
from jsonfield import JSONField

# validators
from app.validators import validate_timeline, validate_members
# for saving timelines
import operator
import json
# import category constants 
import app.categories as cate




# Article Models
class Article(models.Model):
    created =  models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    summary = models.TextField()
    link = models.URLField()
    tags = JSONField(default=[])
    category = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ('created',)


# Like Models
class Like(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# Startup Models
class Startup(models.Model):
    # user = models.ForeignKey('auth.User', related_name = "startups", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    state = models.PositiveSmallIntegerField(default=0)
    category = models.PositiveSmallIntegerField(choices=cate.CATEGORIES,default=0)
    tags = JSONField(default=[])
    background = models.TextField()
    market = models.TextField()
    solution = models.TextField()
    business_model = models.TextField()
    future = models.TextField()
    raiseAmount = models.PositiveIntegerField(default=0)
    timeline = JSONField(default=[],validators=[validate_timeline])
    location = models.CharField(max_length=50)
    summary = models.CharField(max_length=255)
    members = JSONField(default=[],validators=[validate_members])
    team_desc = models.TextField()
    def save(self, *args, **kwargs):
        timeline_unordered = [dict(data) for data in self.timeline]
        timeline_ordered = sorted(timeline_unordered, key=operator.itemgetter('date')) 
        self.timeline = json.dumps(timeline_ordered)
        super(Startup, self).save(*args, **kwargs)

# Feedback Models
class Feedback(models.Model):
    user = models.ForeignKey('auth.User', related_name = "feedbacks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback =  models.TextField()
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE),
    reply = models.TextField()
