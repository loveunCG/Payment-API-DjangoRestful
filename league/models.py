from django.db import models
from django.utils import timezone
from django.template.defaultfilters import default
from .static import LEAGUES_STATUS, FOLLOWER_STATUS

class Leagues(models.Model):
    manager = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    terms = models.TextField()
    status = models.IntegerField(choices=LEAGUES_STATUS, default=0)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
            return self.name

class Follower(models.Model):
    league= models.ForeignKey('Leagues', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=FOLLOWER_STATUS)
    def __counterLeague(self, league):        
        return self.objects.filter(league=league).count()
    
class Role(models.Model):
    name = models.CharField(max_length = 200)
    created_date =  models.DateTimeField(default=timezone.now)

class Notification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    league = models.ForeignKey('Leagues', on_delete=models.CASCADE)
    created_date =  models.DateTimeField(default=timezone.now)
    status = models.IntegerField()
    

    
