# -*- coding: utf-8 -*-
import click
import logging
import numpy as np
import pandas as pd
import sqlite3
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
# from ...features.build_features import pipeline

def pipeline(df):
    logger = logging.getLogger(__name__)
    logger.info('running preprocessing pipeline...')
    df_ret = df.copy()
    df_ret['committerDate'] = pd.to_datetime(df_ret.committerDate)
    df_ret['committerTimezone'] = df_ret.committerTimezone.astype('int')
    df_ret['committerDateLocal'] = df_ret.apply(lambda x: x.committerDate + np.timedelta64(x.committerTimezone,'s'), axis=1)
    week_days = df_ret.committerDateLocal.dt.dayofweek
    df_ret = pd.concat([df_ret, pd.get_dummies(week_days, prefix='dayOfWeek')], axis=1)
    df_ret['committerHourOfDay'] = df_ret.committerDateLocal.apply(lambda x: x.hour)
    df_ret.drop(columns=['commitHash', 'committerDate', 'committerDateLocal', 'committerTimezone'], inplace=True)
    df_ret.dropna(axis=0, how='any', inplace=True)
    return df_ret


@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(output_filepath, input_filepath='../../data/raw/technicalDebtDataset.db'):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    conn = sqlite3.connect(input_filepath) # connect to DB
    df = pd.read_sql('SELECT * FROM dataset', conn)
    df_ret = pipeline(df)
    df_ret.to_csv(output_filepath, index=False)
    return 0


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
