from django.db import models


class PriceBars(models.Model):
    datetime_reference = models.DateTimeField()
    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)


class PartialPriceBar(models.Model):
    datetime_reference = models.DateTimeField()
    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
