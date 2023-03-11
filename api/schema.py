import graphene
from django.conf import settings
from api.models import PriceBars, PartialPriceBar, USDBRL
from api.statistics import USDBRLDFHandler
from api.types import DynamicScalar


class USDBRLGroupedStatistic(graphene.ObjectType):
    labels = graphene.List(DynamicScalar)
    mean = graphene.List(graphene.Float)
    variance = graphene.List(graphene.Float)
    positive_std = graphene.List(graphene.Float)
    negative_std = graphene.List(graphene.Float)
    relative_frequency = graphene.List(graphene.Float)
    ewm = graphene.List(graphene.Float)
    diff = graphene.List(graphene.Float)


class USDBRLStatistics(graphene.ObjectType):
    diff = graphene.List(graphene.Float)
    rolling = graphene.List(graphene.Float)
    grouped_by_hour = graphene.Field(USDBRLGroupedStatistic)
    grouped_by_weekday = graphene.Field(USDBRLGroupedStatistic)


class USDBRLType(graphene.ObjectType):
    datetime_reference = graphene.DateTime()
    price = graphene.Float()
    statistics = graphene.Field(USDBRLStatistics)

    def resolve_statistics(self, info, **kwargs):
        df = info.variable_values['dataframe']
        hour_df = USDBRLDFHandler.get_hour_group(df)
        week_df = USDBRLDFHandler.get_weekday_group(df)
        return USDBRLStatistics(
            diff=df.DIFF.values,
            rolling=df.ROLLING.values,
            grouped_by_hour=USDBRLGroupedStatistic(
                mean=hour_df.MEAN.values,
                variance=hour_df.VARIANCE.values,
                positive_std=hour_df.POS_STD.values,
                negative_std=hour_df.NEG_STD.values,
                relative_frequency=hour_df.REL_FREQ.values,
                ewm=hour_df.MEAN.ewm(alpha=.6).mean().values,
                diff=hour_df.DIFF.values,
                labels=hour_df.index.values
            ),
            grouped_by_weekday=USDBRLGroupedStatistic(
                mean=week_df.MEAN.values,
                variance=week_df.VARIANCE.values,
                positive_std=week_df.POS_STD.values,
                negative_std=week_df.NEG_STD.values,
                relative_frequency=week_df.REL_FREQ.values,
                ewm=week_df.MEAN.ewm(alpha=.6).mean().values,
                diff=week_df.DIFF.values,
                labels=week_df.index.values
            )
        )

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

    usd_brl = graphene.List(
        USDBRLType,
        datetime_reference__gte=graphene.Date(),
        datetime_reference__lte=graphene.Date(),
        price__gte=graphene.Float(),
        price__lte=graphene.Float()
    )
    def resolve_usd_brl(self, info, **kwargs):
        records = USDBRL.objects.filter(**kwargs)
        info.variable_values['dataframe'] = USDBRLDFHandler.get_dataframe(records)
        return records
        

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

