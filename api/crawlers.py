from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from api.models import PriceBars, PartialPriceBar, USDBRL


class USDBRLCrawler:
    def __init__(self, url, sleep_secs):
        self.url = url
        self.sleep_secs = sleep_secs

    def get_data(self):
        response = requests.get(self.url)

        if response.status_code != 200:
            print('Error on requesting data with status code ', response.status_code)
            return False

        soup = BeautifulSoup(response.content, 'html.parser')
        value = soup.find(class_='px-last font_xl font_extra_bold margin-xxs-right').text
        if value:
            try:
                USDBRL.objects.create(float(value))
            except Exception as err:
                print('Failed saving USDBRL value with error:')
                print(str(err))

    def run(self):
        while True:
            self.get_data()
            sleep(self.sleep_secs)



class ForexCrawler:
    def __init__(self, url, sleep_secs, session, username):
        self.url = url
        self.sleep_secs = sleep_secs
        self.session = session
        self.username = username


    def get_data(self):
        response = requests.get(
            self.url,
            headers={
                'username': self.username,
                'session': self.session
            }
        )
        if response.status_code != 200:
            print('Error on requesting data with status code ', response.status_code)
            return False

        return response.json()

    def process_price_bars(self, data):
        for price_bar in data:
            dt = self.preprocess_datetime(price_bar['BarDate'])
            try:
                new_price_bar, created = PriceBars.objects.get_or_create(
                    datetime_reference=dt
                )
            except Exception as e:
                print('Error creating price bars with error: ')
                print(str(e))
                continue

            if created:
                new_price_bar.open = price_bar['Open']
                new_price_bar.close = price_bar['Close']
                new_price_bar.low = price_bar['Low']
                new_price_bar.high = price_bar['High']
                new_price_bar.save()


    def process_partial_price_bar(self, data):
        dt = self.preprocess_datetime(data['BarDate'])
        
        try:
            partial_price_bar, created = PartialPriceBar.objects.get_or_create(
                datetime_reference=dt
            )
        except Exception as e:
            print('Error creating partial_price with error: ')
            print(str(e))
            return

        if created:
            partial_price_bar.open = data['Open']
            partial_price_bar.close = data['Close']
            partial_price_bar.low = data['Low']
            partial_price_bar.high = data['High']
            partial_price_bar.save()


    def preprocess_datetime(self, raw_datetime):
        return datetime.fromtimestamp(int(raw_datetime.split('(')[1].split(')')[0][:10]))

    def run(self):
        while True:

            data = self.get_data()
            if data:
                self.process_partial_price_bar(data['PartialPriceBar'])
                self.process_price_bars(data['PriceBars'])

            sleep(self.sleep_secs)
