import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


import pickle

# to load dataset
data = pd.read_csv("dataset/diseasedataset.csv")
x = data.drop("disease", axis=1)
y = data["disease"]

model = RandomForestClassifier()
model.fit(x,y)

#to save model
with open("models/disease_model.pkl","wb") as f:
    pickle.dump(model,f)
print("Model trained successfully")