import pandas as pd
# from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
import joblib
import numpy as np

X = pd.read_csv('X.csv')
Y = pd.read_csv('Y.csv')

X_train, X_test, y_train, y_test = train_test_split(X,Y,train_size=0.80, test_size=0.20,random_state=42)


exported_pipeline = ExtraTreesRegressor(bootstrap=False, max_features=0.8, min_samples_leaf=4, min_samples_split=3, n_estimators=100)
exported_pipeline.fit(X_train, y_train)

filename = 'model_Air.sav'
joblib.dump(exported_pipeline, filename)

X =[[81.40,	124.50,	1.44	,20.50,	12.08,	10.72,	0.12	,15.24	,127.09	,0.20	,6.50	,0.06]]

loaded_model = joblib.load(filename)

answer = loaded_model.predict(X)
print(answer[0])
# print("Hello")