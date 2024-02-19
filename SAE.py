import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt



#chargement des données

client = pd.read_csv('clients_greendwell.csv')
historiques = pd.read_excel('historique_acces_greendwell.xlsx')


#Conversion en data frames de données chargées
client = pd.DataFrame(client)
historiques = pd.DataFrame(historiques)

print(client.head())

print(historiques.head())


