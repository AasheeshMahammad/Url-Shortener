from django.db import models

# Create your models here.

from shortener.models import Shortt

class ClickEventManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, Shortt):
            obj, created = self.get_or_create(shortt_url=instance)
            obj.count += 1
            obj.save()
            return obj.count

class ClickEvent(models.Model):
    shortt_url = models.OneToOneField(Shortt, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ClickEventManager()

    def __str__(self):
        return str(self.shortt_url)
    

