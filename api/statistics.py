import pandas as pd


class USDBRLDFHandler:

    @staticmethod
    def get_dataframe(data):
        df = pd.DataFrame(
            [(i.price, i.datetime_reference) for i in data],
            columns=['price', 'datetime_reference']
        )
        df.set_index(pd.to_datetime(df.datetime_reference), inplace=True)
        df['DIFF'] = df.price.diff().fillna(0)
        df['ROLLING'] = df.price.rolling(8).mean().fillna(0)
        return df

    @staticmethod
    def get_hour_group(dataframe):
        df = dataframe.copy()
        index_count = dataframe.index.value_counts(normalize=True)
        hour_df = USDBRLDFHandler.get_satistics(
            df.groupby(df.index.hour),
            index_count
        )
        return hour_df

    @staticmethod
    def get_weekday_group(dataframe):
        df = dataframe.copy()
        index_count = dataframe.index.value_counts(normalize=True)
        week_df = USDBRLDFHandler.get_satistics(
            df.groupby(df.index.strftime('%A')),
            index_count
        )
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week_df.reindex(days)
        return week_df

    @staticmethod
    def get_satistics(dataframe, index_count):
        df = pd.DataFrame()
        df['MEAN'] = dataframe.price.mean()
        df['VARIANCE'] = dataframe.price.var()
        df['DIFF'] = dataframe.price.diff().fillna(0)
        df['REL_FREQ'] = df.DIFF / df.DIFF.sum()
        df['F'] = index_count
        df['POS_STD'] = df[['REL_FREQ', 'F']].T.var() + (df.REL_FREQ + df[['REL_FREQ', 'F']].T.std()).clip(0)
        df['NEG_STD'] = df[['REL_FREQ', 'F']].T.var() + (df.REL_FREQ - df[['REL_FREQ', 'F']].T.std()).clip(0)

        # Set percentage columns format
        df['REL_FREQ'] = df.REL_FREQ * 100
        df['POS_STD'] = df.POS_STD * 100
        df['NEG_STD'] = df.NEG_STD * 100

        # Show aonly 2 decimal float points
        df['REL_FREQ'] = df.REL_FREQ.round(2)
        df['POS_STD'] = df.POS_STD.round(2)
        df['NEG_STD'] = df.NEG_STD.round(2)

        return df.fillna(0)
