import pickle
import pandas as pd

with open('model_lr.pickle', 'rb') as f:
    model_pipe = pickle.load(f)

x  = input('give me some lyrics:')
x= pd.DataFrame({'index':1,'Lyrics': x }, index=[1])
print(model_pipe.predict(x))
print(model_pipe.predict_proba(x))
