import pandas as pd
# from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
import joblib
import numpy as np

X = pd.read_csv('X.csv')
Y = pd.read_csv('Y.csv')

X_train, X_test, y_train, y_test = train_test_split(X,Y,train_size=0.80, test_size=0.20,random_state=42)


exported_pipeline = ExtraTreesClassifier()
exported_pipeline.fit(X_train, y_train)

filename = 'model.sav'
joblib.dump(exported_pipeline, filename)

X =[[195.102299,	17404.177061,	7.509306,	327.459760,	16.140368	,2.309149	]]

loaded_model = joblib.load(filename)

answer = loaded_model.predict(X)
print(answer[0])
# print("Hello")