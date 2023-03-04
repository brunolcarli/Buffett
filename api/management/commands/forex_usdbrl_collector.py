from django.core.management.base import BaseCommand
from django.conf import settings
from api.crawlers import ForexCrawler


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        print('Starting FOrex USD->BRL daemon')
        params = settings.FOREX_CREDENTIALS
        daemon = ForexCrawler(**params)

        daemon.run()
