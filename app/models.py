from django.db import models
from jsonfield import JSONField
from .validators import validate_timeline

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
    user = models.ForeignKey('auth.User', related_name = "startups", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    state = models.PositiveSmallIntegerField(default=0)
    category = models.PositiveSmallIntegerField(default=0)
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
    members = JSONField(default=[])
    team_desc = models.TextField()
    #feedback = models.ListField()

# Feedback Models
class Feedback(models.Model):
    user = models.ForeignKey('auth.User', related_name = "feedbacks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback =  models.TextField()
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE),
    reply = models.TextField()
