import pandas as pd
import numpy as np


#Importer les données
df_client = pd.read_csv('clients_greendwell.csv')
df_service = pd.read_excel('historique_acces_greendwell.xlsx', sheet_name='Services Consommes')
