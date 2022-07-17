from django.core.management import BaseCommand, CommandError

from shortener.models import Shortt

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)
    
    def handle(self,*args, **options):
        return Shortt.objects.refresh_shortcodes(items=options['items'])