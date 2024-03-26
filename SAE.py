import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt



'''Étape N°1 : Collecter les données'''
 

#chargement des données

client = pd.read_csv('clients_greendwell.csv')

#Conversion en data frames de données chargées
client = pd.DataFrame(client)
#historiques = pd.DataFrame(historiques)

# Affichons les premières lignes du DataFrame
print(client.head())

#print(historiques.head())


''' Étape N°2 : Nettoyer les données'''


#Phase de nettoyage des données Clients


##visualisation nos differents types de données 

print(client.dtypes)  #J'ai remarqué que les attributs Date Inscription et Data Annulation n'etaient pas 
#bien typé d'ou on les rend en type date time 

print(client.columns)

print('Le jeu des clients a une taille de :',client.shape)


## Convertir les colonnes de dates au format approprié

### Conversion des colonnes Data Inscription et Date d'Annulation en datetime

client['Date Inscription'] = pd.to_datetime(client['Date Inscription'])
client['Date Annulation'] = pd.to_datetime(client['Date Annulation'])

print(client.dtypes) # Pour verifier si le type a changé

## Traitement des anomalies sur les colonnes

### Traitement de la colonne Taux Abonnement

# Conversion de la colonne 'Taux Abonnement' en une colonne numérique

print(client['Taux Abonnement'].head(3))

# convertion du type de taux d abonnement en numerique qui sera float
# et remplacement du symbole € par le vide genre on le supprime et on remplace le 112.99 par 2.99 pour eco basique
client['Taux Abonnement'] = client['Taux Abonnement'].replace({'€': '', '112.99' : '2.99'}, regex=True).astype(float)



### Traitement de la colonne Remise

# Convertision la colonne 'Remise' en une colonne binaire (car il y'a des oui )
client['Remise'] = client['Remise'].apply(lambda x: 1 if x == 'Oui' else 0) #il y'avait des nan dans Remise 
# ca  remplace les nan par 0 c'est pourquoi plus bas il y'a plus de valeurs manquantes sur cette colonne



### Traitement de la colonne plan
# Ici on va remplacer les valeurs manquantes par le plan Eco Basique vu que par defaut le plan 
#pour tout utilisateur est Eco Basique

print(client['Plan'].head())
# Remplacement des valeurs manquantes dans la colonne 'Plan' par le plan Eco Basique
client['Plan'] = client['Plan'].fillna('Éco Basique')



### Traitement de la colonne Email

#L'on remarque la presence de plus d'un arobase dans nos emails et on veut donc le supprimer
# Fonction pour corriger les adresses e-mail
def corriger_email(email):
    # Si l'adresse e-mail contient plus d'un caractère '@', supprimer le deuxième '@'
    if email.count('@') > 1:
        index_dernier_arobase = email.rfind('@')
        email = email[:index_dernier_arobase] + email[index_dernier_arobase+1:]
    
    return email


# Appliquons la fonction de correction sur la colonne 'Email'
client['Email'] = client['Email'].apply(corriger_email)



### Pour les valeurs manquantes de la colonne Date Annulation on ne peut pas les remplacer car ca signifie 
# que le client n'a pas annulé son forfait


## Traitement et Gestion des valeurs manquantes et duplicats

### Vérification des données manquantes
# On utilise client.isnull().sum() pour vérifier s'il y a des valeurs manquantes dans chaque colonne
# Relais de cette partie pour vérifier si des valeurs manquantes ont été correctement traitées

print("Nombre de valeurs manquantes dans chaque colonne :")
print(client.isnull().sum())

#On remarque que les valeurs manquantes ont été bien traitées. 
#Les 79 valeurs manquantes dans la colonne Date Annulation signifie que 79 clients n'ont pas encore
#annulés leur abonnement


### Vérification des lignes dupliquées
# On utilise client.duplicated().sum() pour vérifier s'il y a des lignes dupliquées
# Relais de cette partie pour vérifier si des lignes dupliquées existent dans le DataFrame
print("Nombre de lignes dupliquées :")
print(client.duplicated().sum())
#Pas de lignes dupliquées


# Vérifier les valeurs uniques pour repérer les incohérences
print("Valeurs uniques :\n", client.nunique())

#Interprétation des valeurs uniques :
#- Il y a 200 valeurs uniques pour les ID clients, ce qui indique qu'aucun ID client n'est identique.
#- Il y a 199 valeurs uniques pour les noms des clients, ce qui peut suggérer qu'il y a deux clients ayant des noms identiques.
#- Il y a 150 dates d'inscription uniques, ce qui pourrait signifier que 50 clients se sont inscrits le même jour. Parallèlement, la colonne de la date d'annulation montre qu'il y a 114 valeurs uniques, indiquant que des annulations ont eu lieu à des dates différentes.
#- Il y a 3 valeurs uniques pour le plan, représentant nos trois plans différents, de même pour les taux d'abonnement.
#- Pour la colonne de remise, il y a deux valeurs uniques, ce qui indique qu'un client peut bénéficier d'une remise ou non.



#L'on peut aussi voir que l'on a pas de lignes dupliquées ou de doublons
print(client.info()) 
print(client.dtypes) 
#L'on peut donc voir qu'a part la colonne Date Annulation ont a bien toujours 200 entrées sur 200 entrées 
#L'on peut aussi voir que les types ont été bien traités



### Vérification des statistiques descriptives pour identifier les valeurs aberrantes
# On utilise client.describe() pour obtenir des statistiques descriptives
# Relais de cette partie pour identifier les valeurs aberrantes dans les données

print("Statistiques descriptives :")
print(client.describe())

#Visualisation des valeurs aberrantes

def afficher_boxplots(df):
    # Sélectionner les colonnes numériques à l'exception de 'ID Client'
    colonnes_numeriques = df.select_dtypes(include=['int64', 'float64']).columns.drop('ID Client')

    # Afficher des boxplots pour chaque colonne numérique
    for colonne in colonnes_numeriques:
        plt.figure(figsize=(8, 6))
        plt.boxplot(df[colonne])
        plt.title(f'Boxplot de {colonne}')
        plt.xlabel(colonne)
        plt.ylabel('Valeurs')
        plt.show()

# Appelons la fonction avec votre DataFrame client
afficher_boxplots(client)

#L'absence de valeurs aberrantes dans nos données, comme indiqué par l'observation des boxplots, témoigne de
#la cohérence et de la fiabilité de nos données. Cela renforce notre confiance dans la qualité de notre 
#ensemble de données et confirme sa robustesse pour les analyses statistiques à venir. 

## Ajout de la colonne "Resiliation" en utilisant numpy.where()

client['Resiliation'] = np.where(client['Date Annulation'].notnull(), 1, 0)
#la valeur 1 dans la colonne "Résiliation" indique qu'un client a résilié son abonnement.
#la valeur 0 dans la colonne "Résiliation" indique qu'un client n'a pas résilié son abonnement.




'''  Étape N°3 : Explorer vos données '''


# Calcul de la durée de l'abonnement avant résiliation

# Calcul de la durée de l'abonnement avant résiliation
# Pour les clients ayant résilié leur abonnement
clients_resilies = client[client['Resiliation'] == 1]
clients_non_resilies = client[client['Resiliation'] == 0]
clients_resilies['Durée Avant Resiliation'] = clients_resilies['Date Annulation'] - clients_resilies['Date Inscription']

# Analyse des clients avec remise ayant résilié
# Nombre de clients avec remise ayant résilié leur abonnement
clients_resilies_avec_remise = clients_resilies[clients_resilies['Remise'] == 1]
nb_clients_resilies_avec_remise = len(clients_resilies_avec_remise)

# Nombre total de clients ayant résilié leur abonnement
nb_total_clients_resilies = len(clients_resilies)
nb_total_clients_non_resilies = len(clients_non_resilies)

# Comparer le pourcentage de clients avec remise ayant résilié leur abonnement avec ceux qui ont résilié sans remise et ceux qui n'ont pas résilié mais ont bénéficié d'une remise
# Nombre de clients sans résiliation ayant bénéficié d'une remise
clients_non_resilies_avec_remise = client[(client['Resiliation'] == 0) & (client['Remise'] == 1)]
nb_clients_non_resilies_avec_remise = len(clients_non_resilies_avec_remise)

# Nombre de clients sans résiliation n'ayant pas bénéficié d'une remise
clients_non_resilies_sans_remise = client[(client['Resiliation'] == 0) & (client['Remise'] == 0)]
nb_clients_non_resilies_sans_remise = len(clients_non_resilies_sans_remise)

# Calcul des pourcentages
pourcentage_clients_resilies_avec_remise = (nb_clients_resilies_avec_remise / nb_total_clients_resilies) * 100
pourcentage_clients_non_resilies_avec_remise = (nb_clients_non_resilies_avec_remise / nb_total_clients_non_resilies) * 100
pourcentage_clients_non_resilies_sans_remise = (nb_clients_non_resilies_sans_remise / nb_total_clients_resilies) * 100

# Affichage des résultats
print("Pourcentage de clients avec remise ayant résilié leur abonnement :", pourcentage_clients_resilies_avec_remise)
print("Pourcentage de clients avec remise n'ayant pas résilié leur abonnement :", pourcentage_clients_non_resilies_avec_remise)
print("Pourcentage de clients sans remise n'ayant pas résilié leur abonnement par rapport aux resilies :", pourcentage_clients_non_resilies_sans_remise)

#Les résultats suggèrent que l'offre de remises semble jouer un rôle significatif dans la rétention des clients.
 #En effet, le pourcentage élevé de résiliation parmi les clients bénéficiant de remises (environ 96.69%) 
# indique que ces remises ne sont peut-être pas aussi efficaces pour fidéliser les clients qu'on pourrait le 
 #penser. En revanche, le pourcentage plus bas de résiliation parmi les clients sans remise (environ 31.65%) 
 #suggère que ces clients sont potentiellement plus fidèles à l'entreprise. Cependant, il est important de noter
 #que même parmi les clients sans remise, un pourcentage significatif (environ 44.63%) a tout de même résilié 
 #leur abonnement, ce qui montre que d'autres facteurs peuvent également influencer la décision de résilier. 
 



##Quelques Visualisations



def plot_pie_chart(labels, sizes, title):
    """Affiche un diagramme à secteurs."""
    colors = ['lightcoral', 'lightskyblue']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()

def plot_histogram(data, title, xlabel, ylabel):
    """Affiche un histogramme."""
    plt.hist(data, bins=20, color='skyblue', edgecolor='black')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

# Appel des fonctions avec les données pertinentes
plot_histogram(clients_resilies['Durée Avant Resiliation'].dt.days, 
               'Distribution de la durée avant résiliation pour les clients ayant résilié', 
               'Durée avant résiliation (jours)', 
               'Nombre de clients')

plot_pie_chart(['Avec remise', 'Sans remise'], 
               [nb_clients_resilies_avec_remise, len(clients_resilies) - nb_clients_resilies_avec_remise], 
               'Répartition des clients ayant résilié selon la présence de remise')

plot_pie_chart(['Avec remise', 'Sans remise'], 
               [nb_clients_non_resilies_avec_remise, len(clients_non_resilies) - nb_clients_non_resilies_avec_remise], 
               'Répartition des clients n\'ayant pas résilié selon la présence de remise')

# Données pour le diagramme à secteurs de ceux qui n'ont pas résiliés et sans remise par rapport aux résiliés
labels = ['Clients sans remise n\'ayant pas résilié', 'Clients résiliés']
sizes = [pourcentage_clients_non_resilies_sans_remise, 100 - pourcentage_clients_non_resilies_sans_remise]

# Appel de la fonction pour afficher le diagramme à secteurs
plot_pie_chart(labels, sizes, 'Répartition des clients sans remise n\'ayant pas résilié par rapport aux résiliés')










#######PARTIE HAOMING#######################

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
