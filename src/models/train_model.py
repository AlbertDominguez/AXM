import joblib
import numpy as np
import pandas as pd
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

def read_and_split():
    df_full = pd.read_csv('../../data/processed/processed_data.csv')
    pos = df_full[df_full.faultInducingBool == 1].copy().reset_index(drop=True)
    neg = df_full[df_full.faultInducingBool == 0].sample(n=1000, random_state=42)
    neg.dropna(inplace=True)
    df_red = pd.concat([neg, pos], axis=0)
    X = df_red.drop(columns='faultInducingBool').to_numpy()
    y = df_red.faultInducingBool.to_numpy()
    trX, valX, trY, valY = train_test_split(X, y, test_size=0.25, random_state=42)
    return trX, valX, trY, valY, df_red.drop(columns='faultInducingBool').columns

def launch_training():
    trX, valX, trY, valY, colnames = read_and_split()
    clf = RandomForestClassifier(n_estimators=500, max_depth=8, random_state=42)
    clf.fit(trX, trY)
    print('Training confusion matrices:\n', confusion_matrix(trY, clf.predict(trX)))
    print('Validation confusion matrices:\n', confusion_matrix(valY, clf.predict(valX)))
    print('Importances:')
    for i in range(len(colnames)):
        print(colnames[i], clf.feature_importances_[i])
    print('Saving model...')
    joblib.dump(clf, '../../models/random_forest.joblib')
    return 0

def main():
    return launch_training()

if __name__ == '__main__':
    sys.exit(main())