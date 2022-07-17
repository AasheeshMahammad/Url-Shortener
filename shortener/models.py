from django.db import models
from .utils import create_shortcode
from django.conf import settings
from .validators import validate_url, validate_dot_com
from django_hosts.resolvers import reverse

# Create your models here.

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class ShorttMananger(models.Manager):

    def all(self, *args, **kwargs):
        qs = super(ShorttMananger, self).all(*args, **kwargs)
        qs_online = qs.filter(active=True)
        return qs_online
    
    def refresh_shortcodes(self, items=None):
        qs = Shortt.objects.filter(id__gte=1)
        if items is not None and isinstance(items,int):
            qs = qs.order_by('-id')[:items]
        count = 0
        for data in qs:
            data.shortcode = create_shortcode(data)
            data.save()
            count += 1
        return f"Count : {count}"

class Shortt(models.Model):
    url = models.CharField(max_length=255, validators=[validate_url, validate_dot_com])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    objects = ShorttMananger()


    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        if 'http' not in self.url:
            self.url = 'http://' + self.url
        super(Shortt, self).save(*args, **kwargs)
 
    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse('shortcode', kwargs={'shortcode':self.shortcode}, host='www', scheme='http')
        return url_path