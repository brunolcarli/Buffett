from django.core.management.base import BaseCommand
from api.crawlers import USDBRLCrawler


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        print('Starting USDBRL daemon')
        daemon = USDBRLCrawler(
            'https://www.bloomberglinea.com.br/quote/USDBRL:CUR/',
            3600
        )

        daemon.run()
