# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 20:19:55 2024

@author: win10
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataProcess:
    """
    Initialise l'objet DataProcess avec le chemin du fichier CSV.

    Parametres:
    clients_file : Le chemin vers le fichier CSV contenant les données à analyser.
    hist_service_file: Le chemin vers le fichier XLSX contenant les données à analyser.
    """
    #Collecter les données
    def __init__(self, clients_file, hist_service_file):    
        self.client = pd.read_csv(clients_file)
        self.service = pd.read_excel(hist_service_file, sheet_name="Services Consommes")
        self.infoLogin = pd.read_excel(hist_service_file, sheet_name="Sessions Login")
        self.histService = pd.read_excel(hist_service_file, sheet_name="Historique Services")
        self.data_historique = None
        
    """
    Effectue la phase de nettoyage des données.

    Cette méthode ne prend pas d'entrée et ne renvoie rien en sortie.
    """
    def nettoyer_donnees(self):
        self.convertir_dates()
        self.convertir_numeric()
        self.gerer_valeurs_manquantes_doublons()
        self.join_tables()
        self.process_lig_aberrant()
        self.test_traitement()
    
    #Convertit les colonnes de dates au format datetime.
    def convertir_dates(self):
        self.infoLogin['Date Heure']=pd.to_datetime(self.infoLogin['Date Heure'])
        self.client['Date Inscription'] = pd.to_datetime(self.client['Date Inscription'])
        
    #Convertit les colonnes de services au format numeric.
    def convertir_numeric(self):
        self.service["ID Service"] = pd.to_numeric(self.service['ID Service'].str.replace('Service',''))
        self.histService["ID Service"] = pd.to_numeric(self.histService['ID Service'].str.replace('Service',''))
    
    #Gère les valeurs manquantes et les doublons dans le DataFrame.
    def gerer_valeurs_manquantes_doublons(self):
        print("Nombre de valeurs manquantes dans table service :", self.service.isnull().sum())
        print("Nombre de valeurs manquantes dans table information session login :", self.infoLogin.isnull().sum())
        print("Nombre de valeurs manquantes dans table historique service :", self.histService.isnull().sum())
        
        print("Nombre de lignes dupliquées dans table service :", self.service.duplicated().sum())
        print("Nombre de lignes dupliquées dans table information session login :", self.infoLogin.duplicated().sum())
        print("Nombre de lignes dupliquées dans table historique service :", self.histService.duplicated().sum())
        
        print("Nombre de plan d\'abonnement utilisés :", self.service['Type Service'].value_counts())
        print("Nombre de services utilisés :", self.histService['ID Service'].value_counts().sort_index())
        
    #Joindre les tables
    def join_tables(self):
        self.data_historique = self.service.merge(self.histService, 'outer', 'ID Service')
        self.data_historique = self.data_historique.merge(self.infoLogin, 'outer', 'ID Session')
        self.data_historique = pd.merge(self.data_historique, self.client[['ID Client', 'Date Inscription']],
                                        on='ID Client', how='left')
        
    #Traite les valeurs aberrantes
    def process_lig_aberrant(self):
        lig_aberrant = self.data_historique[self.data_historique['Date Heure'].dt.date < self.data_historique['Date Inscription']]
        print("Nombre des lignes aberante : ", len(lig_aberrant))
        df_premier_session = self.data_historique.groupby('ID Client')['Date Heure'].min().reset_index()
        self.data_historique['Date Inscription'] = np.where(self.data_historique['ID Client'].isin(lig_aberrant['ID Client']),
                                                            self.data_historique['ID Client'].map(df_premier_session.set_index('ID Client')['Date Heure'].dt.date),
                                                            self.data_historique['Date Inscription'])
        
       
    """
    Teste le traitement des colonnes en vérifiant les valeurs après nettoyage.

    Cette méthode ne prend pas d'entrée et ne renvoie rien en sortie.
    """
    def test_traitement(self):
        #Affichage des types de données après nettoyage
        print("Types de données après nettoyage :")
        print(self.service.dtypes)
        print(self.infoLogin.dtypes)
        print(self.histService.dtypes)

        #Affichage des lignes abérrants après nettoyage
        self.data_historique['Date Inscription'] = pd.to_datetime(self.data_historique['Date Inscription'])
        lig_aberrant_traitee = self.data_historique[self.data_historique['Date Heure'].dt.date < self.data_historique['Date Inscription']].reset_index()
        print("Nombre des lignes aberante apres traitee : ", len(lig_aberrant_traitee))
    
    "Méthode pour explorer des données"
    def explorer_donnees(self):
        self.nb_session_clients()
        self.nb_interaction_client()
        self.nb_service_utilise()
        self.nb_plan_utilise()
        self.nb_session_par_jour()
        self.nb_session_mois()
        self.nb_session_annee()
             
    #Nombre de session de chaque clients
    def nb_session_clients(self):
        sessions_par_client = self.data_historique.groupby('ID Client')['Date Heure'].count()
        print("Nombre de session de chaque clients \n", sessions_par_client.sort_values(ascending=False))
        ##Visualisation des données
        plt.figure(figsize=(20, 8))
        sessions_par_client.plot(kind='bar')
        plt.title('Nombre de session par client')
        plt.xlabel('Nombre total de sessions')
        plt.ylabel('ID clients')
        plt.show()
        
    #Nombre d'interaction de différents clients
    def nb_interaction_client(self):
        interactions_par_client = self.data_historique.groupby('ID Client')['Nombre Interactions'].sum()
        print("Nombre d'interaction de différents clients \n", interactions_par_client.sort_values(ascending=False))
        ##Visualisation des données
        plt.figure(figsize=(20, 8))
        interactions_par_client.plot(kind='bar')
        plt.title('Nombre d\'interaction par client')
        plt.xlabel('Nombre total d\'interactions')
        plt.ylabel('ID clients')
        plt.show()
        
    #Nombre de service utilise
    def nb_service_utilise(self):
        service_counts = self.data_historique['ID Service'].value_counts()
        print("Nombre utilisé de différents services \n",service_counts.sort_values(ascending=False))
        ##Visualisation des données
        plt.figure(figsize=(20, 8))
        service_counts.plot(kind='bar')
        plt.title('Nombre utilisé de différents sevices')
        plt.xlabel('Service')
        plt.ylabel('Nombre de fois utilisé')
        plt.xticks(rotation=360)
        plt.show()
        
    #Nombre de plan d'abonnement
    def nb_plan_utilise(self):
        plan_counts = self.data_historique['Type Service'].value_counts()
        print("Nombre utilisé de différent plan d'abonnement \n",plan_counts)
        ##Visualisation des données
        plt.figure(figsize=(20, 8))
        plan_counts.plot(kind='bar')
        plt.title('Nombre utilsé de différents plans d\'abonnement ')
        plt.xlabel('Type de plan d\'abonnement')
        plt.ylabel('Nombre de fois choisisé')
        plt.xticks(rotation=360)
        plt.show()
        
    #Nombre de session dans différent jour
    def nb_session_par_jour(self):
        sessions_par_jour = self.data_historique['Date Heure'].dt.date.value_counts().sort_index()
        print("Nombre de session dans different jours: \n", sessions_par_jour.sort_values(ascending=False))
        print("Nombre moyenne de session dans un jours:", sessions_par_jour.mean())
        ##Visualisation des données
        plt.figure(figsize=(20, 8))
        sessions_par_jour.plot(kind='line')
        plt.title('Nombre de session dans différent jours')
        plt.xlabel('Date')
        plt.ylabel('Nombre de session')
        plt.show()
        
    # Nombre de session dans un mois
    def nb_session_mois(self):
        sessions_par_mois = self.data_historique['Date Heure'].dt.to_period('M').value_counts().sort_index()
        print("Nombre de session dans different mois: \n", sessions_par_mois.sort_values(ascending=False))
        print("Nombre moyenne de session dans un mois:", sessions_par_mois.mean())
        ##Visualisation des données
        plt.figure(figsize=(20, 8))
        sessions_par_mois.plot(kind='line')
        plt.title('Nombre de session dans différent mois')
        plt.xlabel('Mois')
        plt.ylabel('Nombre de session')
        plt.show()


    # Nombre de session dans une annee
    def nb_session_annee(self):
        sessions_par_annee = self.data_historique['Date Heure'].dt.to_period('Y').value_counts().sort_index()
        print("Nombre de session dans different année: \n", sessions_par_annee.sort_values(ascending=False))
        print("Nombre moyenne de session dans une année:", sessions_par_annee.mean())
        ##Visualisation des données
        plt.figure(figsize=(20, 8))
        sessions_par_annee.plot(kind='line')
        plt.title('Nombre de session dans différent mois')
        plt.xlabel('Année')
        plt.ylabel('Nombre de session')
        plt.show()

if __name__ == "__main__":
    data_processor = DataProcess('clients_greendwell.csv', 'historique_acces_greendwell.xlsx')
    data_processor.nettoyer_donnees()
    data_processor.explorer_donnees()

# Créer un DataFrame avec les informations demandées pour chaque client
df_modelisation = pd.DataFrame()

# Ajouter les colonnes 
df_modelisation['ID Client'] = data_processor.client['ID Client']
df_modelisation['Annulation'] = data_processor.client['Date Annulation'].notnull().astype(int)
df_modelisation['Remise'] = data_processor.client['Remise'].apply(lambda x: 1 if x == 'Oui' else 0)

# Calculer le nombre de sessions par client
sessions_par_client = data_processor.data_historique.groupby('ID Client')['Date Heure'].count()
df_modelisation = df_modelisation.merge(sessions_par_client, how='left', left_on='ID Client', right_index=True)
df_modelisation.rename(columns={'Date Heure': 'Nombre Session'}, inplace=True)
df_modelisation['Nombre Session'] = df_modelisation['Nombre Session'].fillna(0)

# Calculer le pourcentage d'utilisation de chaque type de plan par client
plans_par_client = data_processor.data_historique.groupby(['ID Client', 'Type Service'])['ID Service'].count().unstack(fill_value=0)
plans_par_client = plans_par_client.div(plans_par_client.sum(axis=1), axis=0) * 100
df_modelisation = df_modelisation.merge(plans_par_client, how='left', left_on='ID Client', right_index=True)
df_modelisation.rename(columns={'Eco Basique': 'Pourcentage plan basique', 'Eco Confort': 'Pourcentage plan confort', 
                                'Eco Premium':'Pourcentage plan premium'}, inplace=True)
df_modelisation[['Pourcentage plan basique','Pourcentage plan confort','Pourcentage plan premium']] = df_modelisation[['Pourcentage plan basique', 'Pourcentage plan confort', 'Pourcentage plan premium']].fillna(0)

# Afficher les premières lignes du DataFrame
print(df_modelisation.head())
