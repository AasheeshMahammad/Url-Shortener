from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
from .models import Shortt
from django.template import loader
from .forms import SubmitUrlForm
from analytics.models import ClickEvent
import json

# Create your views here.

class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        form = SubmitUrlForm()
        template = loader.get_template('home.html')
        context = {'form':form,}
        return HttpResponse(template.render(context,request))
    
    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {'form':form}
        page = 'home.html'
        if form.is_valid():
            url = form.cleaned_data.get('url')
            if 'http' not in url:
                url = 'https://'+url
            obj, created = Shortt.objects.get_or_create(url=url)
            if request.POST.get('simple'):
                data = {'short_url':obj.get_short_url()}
                return HttpResponse(json.dumps(data))
            context = {'object':obj,'created':created}
            if created:
                page = 'created.html'
            else:
                page = 'existing.html'
        if request.POST.get('simple'):
            return HttpResponseBadRequest("Invalid URL")
        template = loader.get_template(page)
        return HttpResponse(template.render(context,request))

class URLRedirectView(View):

    def get(self, request, shortcode, *args, **kwargs):
        obj = get_object_or_404(Shortt, shortcode=shortcode)
        obj_url = obj.url
        count = ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj_url)
