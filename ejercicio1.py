import pandas as pd

df = pd.read_csv("titanic.csv")

df["Cabin"] = df["Cabin"].fillna("Desconocido")

sex = {"male":"M","female":"F"}

df["Sex"] = df["Sex"].apply(lambda x: sex[x])

#print(df.shape)
#print(df.count())
#print(df.describe())
#print(df["Sex"].head())
#print(df["Sex"].value_counts())
print(df.groupby(["Sex"])["Survived"].mean()*100)
