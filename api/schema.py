import graphene
from django.conf import settings
from api.models import PriceBars, PartialPriceBar



class PriceBarsType(graphene.ObjectType):
    datetime_reference = graphene.DateTime()
    open = graphene.Float()
    close = graphene.Float()
    high = graphene.Float()
    low = graphene.Float()


class PartialPriceBarType(graphene.ObjectType):
    datetime_reference = graphene.DateTime()
    open = graphene.Float()
    close = graphene.Float()
    high = graphene.Float()
    low = graphene.Float()



class Query:
    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return settings.VERSION


    price_bars = graphene.List(
        PriceBarsType,
        # date filters
        datetime_reference__gte=graphene.Date(),
        datetime_reference__lte=graphene.Date(),
        # open filters
        open__gte=graphene.Float(),
        open__lte=graphene.Float(),
        # close filters
        close__gte=graphene.Float(),
        close__lte=graphene.Float(),
        # high filters
        high__gte=graphene.Float(),
        high__lte=graphene.Float(),
        # low
        low__gte=graphene.Float(),
        low__lte=graphene.Float()

    )
    def resolve_price_bars(self, info, **kwargs):
        return PriceBars.objects.filter(**kwargs)

    partial_price_bar = graphene.List(
        PriceBarsType,
        # date filters
        datetime_reference__gte=graphene.Date(),
        datetime_reference__lte=graphene.Date(),
        # open filters
        open__gte=graphene.Float(),
        open__lte=graphene.Float(),
        # close filters
        close__gte=graphene.Float(),
        close__lte=graphene.Float(),
        # high filters
        high__gte=graphene.Float(),
        high__lte=graphene.Float(),
        # low
        low__gte=graphene.Float(),
        low__lte=graphene.Float()
    )
    def resolve_partial_price_bar(self, info, **kwargs):
        return PartialPriceBar.objects.filter(**kwargs)

