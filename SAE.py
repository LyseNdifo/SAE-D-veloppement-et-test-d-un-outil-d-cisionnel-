import pandas as pd


#Importer les données
df_client = pd.read_csv('clients_greendwell.csv')
df_service = pd.read_excel('historique_acces_greendwell.xlsx', sheet_name = "Services Consommes")
df_infoLogin = pd.read_excel('historique_acces_greendwell.xlsx', sheet_name = "Sessions Login")
df_histService = pd.read_excel('historique_acces_greendwell.xlsx', sheet_name = "Historique Services")

#Vérifier les types de différents variables
print(df_service.dtypes)
"""
ID Service      object
Nom Service     object
Type Service    object
Popularite       int64
dtype: object
"""
#ID Service peut etre changer en numeric pour faciliter la tache
print(df_infoLogin.dtypes)
"""
ID Session              int64
Date Heure             object
Nombre Interactions     int64
dtype: object
"""
#Date Heure doit etre forme date
print(df_histService.dtypes)
"""
ID Client         int64
ID Session        int64
ID Service       object
Ordre Service     int64
dtype: object
"""
#ID Service peut etre changer en numeric pour faciliter la tache

#Traitement type de variables
df_service["ID Service"] = pd.to_numeric(df_service['ID Service'].str.replace('Service',''))
print(df_service.dtypes)
df_histService["ID Service"] = pd.to_numeric(df_histService['ID Service'].str.replace('Service',''))
print(df_histService.dtypes)

df_infoLogin['Date Heure']=pd.to_datetime(df_infoLogin['Date Heure'])
print(df_infoLogin.dtypes)

#Vérifier valeurs manquantes
print(df_service.info())
print(df_infoLogin.info())
print(df_histService.info())
#pas de NaN

#Données dupliquées
print(df_service[df_service.duplicated()])
print(df_infoLogin[df_infoLogin.duplicated()])
print(df_histService[df_histService.duplicated()])
#pas de données dupliquées

