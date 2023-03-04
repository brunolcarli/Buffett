from django.db import models


class PriceBars(models.Model):
    datetime_reference = models.DateTimeField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()


class PartialPriceBar(models.Model):
    datetime_reference = models.DateTimeField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
