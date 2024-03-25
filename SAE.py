import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


"""
Importer les données
"""

df_client = pd.read_csv('clients_greendwell.csv')
df_service = pd.read_excel('historique_acces_greendwell.xlsx', sheet_name = "Services Consommes")
df_infoLogin = pd.read_excel('historique_acces_greendwell.xlsx', sheet_name = "Sessions Login")
df_histService = pd.read_excel('historique_acces_greendwell.xlsx', sheet_name = "Historique Services")

"""
Nettoyer les données
"""

# Visualisation les types de données
## Table Services Consommes
print(df_service.dtypes)
#La variable "ID Service" peut être convertir en numeric pour faciliter la calcul

## Table Sessions Login
print(df_infoLogin.dtypes)
#La variable "Date Heure" doit être en forme datetime

## Table Historique Services
print(df_histService.dtypes)
#La variable "ID Service" peut être convertir en numeric pour faciliter la calcul

# Traitement type de variables
## Conversion des colonnes "ID Service" en numeric
df_service["ID Service"] = pd.to_numeric(df_service['ID Service'].str.replace('Service',''))
print(df_service.dtypes)
df_histService["ID Service"] = pd.to_numeric(df_histService['ID Service'].str.replace('Service',''))
print(df_histService.dtypes)

## Conversion la colonne "Date Heure" en datetime
df_infoLogin['Date Heure']=pd.to_datetime(df_infoLogin['Date Heure'])
print(df_infoLogin.dtypes)

# Vérification valeurs manquantes
print(df_service.info())
print(df_infoLogin.info())
print(df_histService.info())
#Pas de valeurs manquantes

# Vérification des textes incohérents et typos(fautes de frappe)
print(df_service['Type Service'].value_counts())
#3 types de service, corresponds à la description dans le sujet

print(df_histService['ID Service'].value_counts().sort_index())
#18 services, corresponds à la description dans le sujet
#En conclusion, pas de donnees incoherents

# Vérification des valeurs abérantes
## La date de session login ne doit pas être avant de la date d'inscription

### Joindre les tables
data = df_service.merge(df_histService,'outer','ID Service')
data = data.merge(df_infoLogin,'outer','ID Session')
df_client['Date Inscription'] =  pd.to_datetime(df_client['Date Inscription'])
data = pd.merge(data, df_client[['ID Client', 'Date Inscription']], on='ID Client', how='left')
print(data.info())

### Trouver des lignes aberrantes
lig_aberrant = data[data['Date Heure'].dt.date < data['Date Inscription']]
print(lig_aberrant['ID Client'].value_counts())
print("Nombre des lignes aberante : ", len(lig_aberrant))

# Traitement données abérantes
## Trouver la date de la première session pour chaque client
df_premier_session = data.groupby('ID Client')['Date Heure'].min().reset_index()

## Remplacer la date d'inscription par la date de la première session login pour les lignes aberrantes
data['Date Inscription'] = np.where(data['ID Client'].isin(lig_aberrant['ID Client']),
                                    data['ID Client'].map(df_premier_session.set_index('ID Client')['Date Heure'].dt.date),
                                    data['Date Inscription'])

## Verifier si les lignes sont bien traitée
data['Date Inscription'] =  pd.to_datetime(data['Date Inscription'])
lig_aberrant2 = data[data['Date Heure'].dt.date < data['Date Inscription']].reset_index()
print("Nombre des lignes aberante apres traitee : ",len(lig_aberrant2))


# Données dupliquées
print(df_service[df_service.duplicated()])
print(df_infoLogin[df_infoLogin.duplicated()])
print(df_histService[df_histService.duplicated()])
#Pas de données dupliquées


"""
#Explorer les données
"""

# Fusioner les données d'historique accès et enlever les colonnes non concernées
data = df_service.merge(df_histService,'outer','ID Service')
data = data.merge(df_infoLogin,'outer','ID Session')
col_conserve = ["ID Service", "Nom Service","Type Service", "ID Client", "ID Session", "Date Heure", "Nombre Interactions"]
data = data[col_conserve]
print(data.info())

# Nombre de session de chaque clients
print("Nombre de session de chaque clients \n",data.groupby('ID Client')['Date Heure'].count().sort_values(ascending=False))

## Diagramme en barres de nombre de session de différents clients
sessions_par_client = data.groupby('ID Client')['Date Heure'].count()
plt.figure(figsize=(20, 8))
sessions_par_client.plot(kind='bar')
plt.title('Nombre de session par client')
plt.xlabel('Nombre total de sessions')
plt.ylabel('ID clients')
plt.show()
#Le nombre le plus élevé de sessions login est celui du client 8187 avec 22 fois. 
#Les clients 3753, 9311, 9208, 7239 et 5428, qui ne se sont connectés qu'une seule fois, 
#sont ceux qui ont le plus petit nombre de sessions.

# Nombre d'interaction de différents clients
print("Nombre d'interaction de différents clients \n",data.groupby('ID Client')['Nombre Interactions'].sum().sort_values(ascending=False))

## Diagramme en barres de nombre d'interaction de différents clients
interactions_par_client = data.groupby('ID Client')['Nombre Interactions'].sum()
plt.figure(figsize=(20, 8))
interactions_par_client.plot(kind='bar')
plt.title('Nombre d\'interaction par client')
plt.xlabel('Nombre total d\'interactions')
plt.ylabel('ID clients')
plt.show()
#Le plus grand nombre d'interactions est encore le client 8187, qui a interagi 619 fois. 
#Le moins nombreux est le client 5428 qui n'a interagi que 8 fois.

# Le service le plus utilise
print("Nombre utilisé de différents services \n",data['ID Service'].value_counts().sort_values(ascending=False))

## Diagramme en barres de nombre d'utilisé de différents sevices
service_counts = data['ID Service'].value_counts()
plt.figure(figsize=(20, 8))
service_counts.plot(kind='bar')
plt.title('Nombre utilisé de différents sevices')
plt.xlabel('Service')
plt.ylabel('Nombre de fois utilisé')
plt.xticks(rotation=360)
plt.show()
#Le service le plus utilisé est le service 5 et 13. 

# Le plan d'abonnement le plus utilise
print("Nombre utilisé de différent plan d'abonnement \n",data['Type Service'].value_counts())

## Diagramme en barres de nombre de choisi de différents plans
plan_counts = data['Type Service'].value_counts()
plt.figure(figsize=(20, 8))
plan_counts.plot(kind='bar')
plt.title('Nombre utilsé de différents plans d\'abonnement ')
plt.xlabel('Type de plan d\'abonnement')
plt.ylabel('Nombre de fois choisisé')
plt.xticks(rotation=360)
plt.show()
#Le plan d'abonnement le plus choisi est le plan Eco Basique (311). 

# Nombre de session dans un jour
print("Nombre de session dans different jours: \n", data['Date Heure'].dt.date.value_counts().sort_values(ascending=False))
print("Nombre moyenne de session dans un jours:", data['Date Heure'].dt.date.value_counts().mean())

## Graphique linéaire de nombre de session dans différents jours
sessions_par_jour = data['Date Heure'].dt.date.value_counts().sort_index()
plt.figure(figsize=(20, 8))
sessions_par_jour.plot(kind='line')
plt.title('Nombre de session dans différent jours')
plt.xlabel('Date')
plt.ylabel('Nombre de session')
plt.show()
#Le 15 septembre 2021 a eu le plus grand nombre de visites avec 15 visites. Ensuite le 15 mars 2021 avec 10 visites.
#Le nombre moyen d'interactions par jour est de 1,85, soit environ deux fois par jour.

# Nombre de session dans un mois
print("Nombre de session dans different mois: \n", data['Date Heure'].dt.to_period('M').value_counts().sort_values(ascending=False))
print("Nombre moyenne de session dans un mois:", data['Date Heure'].dt.to_period('M').value_counts().mean())

## Graphique linéaire de nombre de session dans différents mois
sessions_par_mois = data['Date Heure'].dt.to_period('M').value_counts().sort_index()
plt.figure(figsize=(20, 8))
sessions_par_mois.plot(kind='line')
plt.title('Nombre de session dans différent mois')
plt.xlabel('Mois')
plt.ylabel('Nombre de session')
plt.show()
#Le nombre moyen de session par mois est d'environ 17,64, soit environ 18 sessions.
#Parmi tout, le mois de septembre 2021 a eu le plus grand nombre de sessions login avec 64 sessions. 
#Et le mois de novembre 2023 a eu le plus petit nombre de sessions avec seulement 1 session.
#Il y a une tendance générale à la baisse du nombre de sessions depuis février 2022.

# Nombre de session dans une annee
print("Nombre de session dans different année: \n", data['Date Heure'].dt.to_period('Y').value_counts().sort_values(ascending=False))
print("Nombre moyenne de session dans une année:", data['Date Heure'].dt.to_period('Y').value_counts().mean())

## Graphique linéaire de nombre de session dans différents années
sessions_par_annee = data['Date Heure'].dt.to_period('Y').value_counts().sort_index()
plt.figure(figsize=(20, 8))
sessions_par_annee.plot(kind='line')
plt.title('Nombre de session dans différent mois')
plt.xlabel('Année')
plt.ylabel('Nombre de session')
plt.show()
#On observe une tendance générale à la baisse du nombre de sessions, 
#avec plus de 300 sessions en 2021 et seulement 48 sessions en 2023.
