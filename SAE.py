import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



#chargement des données

client = pd.read_csv('clients_greendwell.csv')
historiques = pd.read_excel('historique_acces_greendwell.xlsx')


#Conversion en data frames de données chargées
client = pd.DataFrame(client)
historiques = pd.DataFrame(historiques)

print(client.head())

print(historiques.head())


#Phase de nettoyage des données Clients


##visualisation nos differents types de données 
print(client.dtypes)  #J'ai remarqué que les attributs Date Inscription et Data Annulation n'etait pas 
#bien typé d'ou on les rend en type date time 

print(client.columns)

print('Le jeu des clients a une taille de :',client.shape)


## Convertir les colonnes de dates au format approprié

### Conversion des colonnes Data Inscription et Date d'Annulation en datetime

client['Date Inscription'] = pd.to_datetime(client['Date Inscription'])
client['Date Annulation'] = pd.to_datetime(client['Date Annulation'])

print(client.dtypes) # Pour verifier si le type a changé


### Traitement de la colonne Taux Abonnement
# Conversion de la colonne 'Taux Abonnement' en une colonne numérique
print(client['Taux Abonnement'].head(3))
# convertion du type de taux d abonnement en numerique qui sera float
# et remplacement du symbole € par le vide genre on le supprime et on remplace le 112.99 par 2.99 pour eco basique
client['Taux Abonnement'] = client['Taux Abonnement'].replace({'€': '', '112.99' : '2.99'}, regex=True).astype(float)


print(client.dtypes) #pour la verification
print(client['Taux Abonnement'].head(3)) #pour la verification



### Traitement et Gestion des valeurs manquantes et duplicats
print(client.info()) # Pour verifier s'il y'a les valeurs manquantes et duplicats etc 

# Vérifier les données manquantes
donnees_manquantes = client.isnull().sum()
print("Données manquantes :\n", donnees_manquantes)  #L'on peut voir que les colonnes 'Plan' et 'Remise' et
       # 'Date Annulation' possede des valeurs manquantes respectivement [15,58,79]

# Vérifier les doublons
doublons = client.duplicated().sum()
print("Doublons :", doublons)  # L'on peut remarquer que dans le DF client il y'a pas de doublons


### Traitement de la colonne Remise
# Convertision la colonne 'Remise' en une colonne binaire (car il y'a des oui )
client['Remise'] = client['Remise'].apply(lambda x: 1 if x == 'Oui' else 0) #il y'avait des nan dans Remise 
#c'est comme si ca les a remplacer par 0 c'est pourquoi plus bas il y'a plus de valeurs manquantes sur cette colonne




### Traitement de la colonne plan
# Ici on va remplacer les valeurs manquantes par le plan Eco Basique vu que par defaut le plan 
#pour tout utilisateur est Eco Basique

print(client['Plan'].head())

# Remplacement des valeurs manquantes dans la colonne 'Plan' par le plan Eco Basique
client['Plan'] = client['Plan'].fillna('Éco Basique')

# Vérifions à nouveau s'il y a des valeurs manquantes dans la colonne 'Plan'
print("Valeurs manquantes dans la colonne 'Plan' après remplacement :", client['Plan'].isnull().sum())


### Pour les valeurs manquantes de la colonne Date Annulation on ne peut pas les remplacer car ca signifie 
# que le client n'a pas annulé son forfait



### Traitement de la colonne Email

# Expression régulière pour extraire les adresses e-mail correctes
pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Fonction pour extraire l'adresse e-mail correcte à partir de la chaîne
def extract_email(text):
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None

# Appliquer la fonction d'extraction à la colonne 'Email'
client['Email'] = client['Email'].apply(extract_email)

# Afficher le DataFrame après la réparation
print(client['Email'].head())


## Valeur aberantes

# boxplot pour la colonne 'Taux Abonnement'  
# on ne voit pas de valeurs aberantes
plt.figure(figsize=(8, 6))
plt.boxplot(client['Taux Abonnement'])
plt.title('Diagramme en boîte de Taux Abonnement')
plt.xlabel('Taux Abonnement')
plt.show()

# Diagramme de dispersion entre 'ID Client' et 'Taux Abonnement'
plt.figure(figsize=(8, 6))
plt.scatter(client['ID Client'], client['Taux Abonnement'])
plt.title('Diagramme de dispersion entre ID Client et Taux Abonnement')
plt.xlabel('ID Client')
plt.ylabel('Taux Abonnement')
plt.show()


## Correlation entre les données
print('Matrice de correlation : \n ',client.corr())

#il n'y a pas de corrélation linéaire significative entre les variables ID Client, Taux Abonnement et Remise.


### Ajout de la colonne "Resiliation" en utilisant numpy.where()
client['Resiliation'] = np.where(client['Date Annulation'].notnull(), 1, 0)

# Afficher les premières lignes du DataFrame pour vérifier
print(client.head())



# Vérifier les statistiques descriptives pour repérer les valeurs aberrantes
print("Statistiques descriptives :\n", client.describe())  # L'on remarque l'ecart type du taux d abonnement 
#est élévé par rapport a la moyenne ce qui implique une dispersion importante des données autour de la moyenne 
# vu sur le plan du Taux d'Abonnement



# Vérifier les valeurs uniques pour repérer les incohérences
print("Valeurs uniques :\n", client.nunique())




