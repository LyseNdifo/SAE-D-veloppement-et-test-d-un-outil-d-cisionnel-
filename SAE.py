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

#Textes incohérents et Typos(fautes de frappe)
print(df_service['Type Service'].value_counts())
print(df_histService['ID Service'].value_counts().sort_index())
#pas de donnees incoherents

#Fusioner les données et enlever les colonnes non concernées
data = df_service.merge(df_histService,'outer','ID Service')
data = data.merge(df_infoLogin,'outer','ID Session')
col_conserve = ["ID Service", "Nom Service","Type Service", "ID Client", "ID Session", "Date Heure", "Nombre Interactions"]
data = data[col_conserve]
print(data.info())

#Valeur abérante
#La date de session login ne doit pas être avant de la dare d'inscription
df_client['Date Inscription'] =  pd.to_datetime(df_client['Date Inscription'])
data = pd.merge(data, df_client[['ID Client', 'Date Inscription']], on='ID Client', how='left')
print(data.info())
lig_aberrant = data[data['Date Heure'].dt.date < data['Date Inscription']]
print(lig_aberrant['ID Client'].value_counts())
print("Nombre des lignes aberante : ", len(lig_aberrant))

#Traitement données abérantes
#Trouver la date de la première session pour chaque client
df_premier_session = data.groupby('ID Client')['Date Heure'].min().reset_index()
# Remplacer la date d'inscription par la date de la première session pour les lignes aberrantes
data['Date Inscription'] = np.where(data['ID Client'].isin(lig_aberrant['ID Client']),
                                    data['ID Client'].map(df_premier_session.set_index('ID Client')['Date Heure'].dt.date),
                                    data['Date Inscription'])
#Verifier
data['Date Inscription'] =  pd.to_datetime(data['Date Inscription'])
lig_aberrant2 = data[data['Date Heure'].dt.date < data['Date Inscription']].reset_index()
print("Nombre des lignes aberante apres traitee : ",len(lig_aberrant2))

#Explorer les données
#Le service le plus utilise
print("Nombre utilise de different service",data['ID Service'].value_counts())

#Nombre de fois qu'un client a accédé au service
print(data['ID Client'].value_counts())

#Nombre de session dans un jour
print("Nombre de session dans different jours:", data['Date Heure'].dt.date.value_counts())
