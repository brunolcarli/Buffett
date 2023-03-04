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


    price_bars = graphene.List(PriceBarsType)
    def resolve_price_bars(self, info, **kwargs):
        return PriceBars.objects.filter(**kwargs)

    partial_price_bar = graphene.List(PriceBarsType)
    def resolve_partial_price_bar(self, info, **kwargs):
        return PartialPriceBar.objects.filter(**kwargs)

