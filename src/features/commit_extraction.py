from datetime import datetime
import json
import numpy as np
import pandas as pd
import pydriller
import sys


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def drill_and_group():
    df = pd.DataFrame()
    for commit in pydriller.RepositoryMining("..").traverse_commits():
        for m in commit.modifications:
            df = df.append([[commit.hash, m.added, m.removed, m.nloc, m.token_count, commit.committer_date, commit.committer_timezone, commit.in_main_branch, m.complexity]])
    df.rename(columns={0: 'commit_hash', 1: 'linesAdded', 2: 'linesRemoved', 3: 'nloc', 4: 'tokenCount', 5: 'committerDate', 6: 'committerTimezone', 7: 'inMainBranch', 8: 'complexity'}, inplace=True)
    df.dropna(inplace=True)
    df['nloc'] = df.nloc.astype('int')
    df['complexity'] = df.complexity.astype('int')
    df['tokenCount'] = df.tokenCount.astype('int')
    grp1 = df.groupby('commit_hash', as_index=False).sum()[['commit_hash', 'nloc', 'linesAdded', 'linesRemoved']]
    grp2 = df.groupby('commit_hash', as_index=False).mean()[['commit_hash', 'tokenCount', 'complexity']]
    grp3 = df.groupby('commit_hash', as_index=False).max()[['commit_hash', 'tokenCount', 'complexity']]
    grp4 = df.groupby('commit_hash', as_index=False).count()
    grp4['changedFiles'] = grp4['linesAdded']
    grp4 = grp4[['commit_hash', 'changedFiles']].copy()
    return df.merge(grp1, how='left', on='commit_hash', suffixes=['', 'total']) \
             .merge(grp2, how='left', on='commit_hash', suffixes=['', 'mean']) \
             .merge(grp3, how='left', on='commit_hash', suffixes=['', 'max']) \
             .merge(grp4, how='left', on='commit_hash', suffixes=['', 'Files']) \
             .drop(columns=['linesAdded', 'linesRemoved', 'nloc', 'tokenCount', 'complexity']) \
             .rename(columns={'linesAddedtotal': 'totalLinesAdded', 'linesRemovedtotal': 'totalLinesRemoved',
                              'complexitymax': 'maxComplexity', 'complexitymean': 'meanComplexity',
                              'tokenCountmean': 'meanTokenCount', 'tokenCountmax': 'maxTokenCount',
                              'nloctotal': 'totalNloc'}) \
             .reset_index(drop=True) \
             .drop_duplicates(subset=['commit_hash'])


def preprocess(df):
    df['committerDate'] = pd.to_datetime(df.committerDate, utc=True)
    df['committerTimezone'] = df.committerTimezone.astype('int')
    df['committerDateLocal'] = df.apply(lambda x: x.committerDate + np.timedelta64(x.committerTimezone,'s'), axis=1)
    week_days = df.committerDateLocal.dt.dayofweek
    df = pd.concat([df, pd.get_dummies(week_days, prefix='dayOfWeek')], axis=1)
    df['committerHourOfDay'] = df.committerDateLocal.apply(lambda x: x.hour)
    df.drop(columns=['committerDate', 'committerDateLocal', 'committerTimezone'], inplace=True)
    df.dropna(axis=0, how='any', inplace=True)
    for i in range(7):
        if 'dayOfWeek_{}'.format(i) not in df.columns:
            df['dayOfWeek_{}'.format(i)] = 0
    return df[['commit_hash', 'inMainBranch', 'maxComplexity', 'meanComplexity', 'totalLinesAdded',
                            'totalLinesRemoved', 'totalNloc', 'maxTokenCount', 'meanTokenCount',
                            'changedFiles', 'dayOfWeek_0', 'dayOfWeek_1', 'dayOfWeek_2',
                            'dayOfWeek_3', 'dayOfWeek_4', 'dayOfWeek_5', 'dayOfWeek_6',
                            'committerHourOfDay']].reset_index(drop=True)


def df_to_json(df, json_filename):
    lst = []
    for i in range(df.shape[0]):
        lst.append(dict())
        for j, col in enumerate(df.columns.tolist()):
            lst[i][col] = df.iloc[i,j] if col != 'inMainBranch' else int(df.iloc[i, j])
    with open(json_filename, 'w') as fb:
        json.dump(lst, fb, cls=NpEncoder)
    print('JSON file dumped to {} successfully!'.format(json_filename))
    return 0
    
def main():
    df = drill_and_group()
    prepr_df = preprocess(df)
    return df_to_json(prepr_df, '../data/processed/{}.json'.format(datetime.today().strftime('%Y-%m-%d')))

if __name__ == '__main__':
    sys.exit(main())
