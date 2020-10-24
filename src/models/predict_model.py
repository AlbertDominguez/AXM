import click
import joblib
import json
import numpy as np
import sys
from sklearn.ensemble import RandomForestClassifier

FEATURE_ORDER = ['inMainBranch', 'maxComplexity', 'meanComplexity', 'totalLinesAdded',
       'totalLinesRemoved', 'totalNloc', 'maxTokenCount', 'meanTokenCount',
       'changedFiles', 'dayOfWeek_0', 'dayOfWeek_1', 'dayOfWeek_2',
       'dayOfWeek_3', 'dayOfWeek_4', 'dayOfWeek_5', 'dayOfWeek_6',
       'committerHourOfDay']
 
def load_model(model_name):
    '''
    Assumes model_name.joblib file exists in the models directory
    '''
    return joblib.load('../../models/{}.joblib'.format(model_name))

def process_json(feat_obj):
    X = np.zeros((len(feat_obj), len(FEATURE_ORDER)))
    for idx in range(len(feat_obj)):
        for i, feature in enumerate(FEATURE_ORDER):
            try:
                X[idx][i] = feat_obj[idx][feature]
            except KeyError as ke:
                ke.args += ('Make sure the data contains all necessary features: {}'.format(FEATURE_ORDER),)
                raise ke
            except Exception as e:
                raise e
    return X

def predict(feat_obj, model_name):
    '''
    Assumes preprocessed data is contained as a dictionary in feat_obj
    '''
    clf = load_model(model_name)
    input_data = process_json(feat_obj)
    return clf.predict(input_data)

def log_preds(preds):
    for i, pred in enumerate(preds):
        if pred:
            print('Entry number {} is predicted to be fault-inducing.'.format(i+1))
        else:
            print('Entry number {} is predicted not to be fault-inducing.'.format(i+1))
    return 0

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('model_name')
def main(input_filepath, model_name):
    with open(input_filepath, 'r') as fb:
        feat_obj = json.load(fb)
    pred = predict(feat_obj, model_name)
    _ = log_preds(pred)
    return 0

if __name__ == '__main__':
    sys.exit(main())