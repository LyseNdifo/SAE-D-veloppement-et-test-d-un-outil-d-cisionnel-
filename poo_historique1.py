# -*- coding: utf-8 -*-
#Importation des librairies necessaires

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt






##------------------------------------------------Lyse-------------------------------------------##


class DataCleaningExploration:
    def __init__(self, data_file):
        """
        Initialise l'objet DataCleaningExploration avec le chemin du fichier CSV.

        Parametres:
        data_file (str): Le chemin vers le fichier CSV contenant les données à analyser.
        """
        self.client = pd.read_csv(data_file)

    # Méthodes de collecte et nettoyage des données (déjà implémentées)

    def collecte_donnees(self):
        """
        Effectue la phase de collecte des données et affiche les premières lignes du DataFrame.
        """
        print(self.client.head())

    def nettoyer_donnees(self):
        """
        Effectue la phase de nettoyage des données.

        Cette méthode ne prend pas d'entrée et ne renvoie rien en sortie.
        """
        self.convertir_dates()
        self.traiter_colonne_taux_abonnement()
        self.traiter_colonne_remise()
        self.traiter_colonne_plan()
        self.traiter_colonne_email()
        self.gerer_valeurs_manquantes_doublons()
        self.test_traitement_colonnes()
        self.afficher_boxplots()

    def convertir_dates(self):
        """
        Convertit les colonnes de dates au format datetime.
        """
        self.client['Date Inscription'] = pd.to_datetime(self.client['Date Inscription'])
        self.client['Date Annulation'] = pd.to_datetime(self.client['Date Annulation'])

    def traiter_colonne_taux_abonnement(self):
        """
        Traite la colonne 'Taux Abonnement' en la convertissant en float et remplacant le '€' par le vide
        et '112.99' par '2.99'
         
        """
        self.client['Taux Abonnement'] = self.client['Taux Abonnement'].replace({'€': '', '112.99': '2.99'}, regex=True).astype(float)

    def traiter_colonne_remise(self):
        """
        Traite la colonne 'Remise'.
        Elle remplace les 'Oui' par 1 et le reste les Nan y compris par 0
        """
        self.client['Remise'] = self.client['Remise'].apply(lambda x: 1 if x == 'Oui' else 0)

    def traiter_colonne_plan(self):
        """
        Traite la colonne 'Plan'.
        Elle remplace toutes les valeurs vides de 'Plan' par 'Éco Basique'
        """
        self.client['Plan'] = self.client['Plan'].fillna('Éco Basique')

    def traiter_colonne_email(self):
        """
        Traite la colonne 'Email'.

        On a remarqué que les adresses email deux arobases donc cette fonction supprime le arobase 
        en trop
        """
        self.client['Email'] = self.client['Email'].apply(self.corriger_email)

    def corriger_email(self, email):
        """
        Corrige les adresses e-mail.

        Parametre:
        email (str): L'adresse e-mail à corriger.

        Retourne:
        str: L'adresse e-mail corrigée.
        """
        if email.count('@') > 1:
            index_dernier_arobase = email.rfind('@')
            email = email[:index_dernier_arobase] + email[index_dernier_arobase+1:]
        return email

    def gerer_valeurs_manquantes_doublons(self):
        """
        Gère les valeurs manquantes et les doublons dans le DataFrame.
        En fait comme on a tout traiter plus haut ici on cherche juste a vérifier s'il y'a plus de missing
        values ou de duplicats
        """
        print("Nombre de valeurs manquantes dans chaque colonne :")
        print(self.client.isnull().sum())
        print("Nombre de lignes dupliquées :", self.client.duplicated().sum())
        print("Valeurs uniques :\n", self.client.nunique())

        self.client['Resiliation'] = np.where(self.client['Date Annulation'].notnull(), 1, 0)
    # Méthode pour tester le traitement des colonnes

    def test_traitement_colonnes(self):
        """
        Teste le traitement des colonnes en vérifiant les valeurs après nettoyage.
         ici on affiche les types de nos colonnes pour vérifier si les types concordent maintenant
         et aussi on affiche les 10 premieres lignes pour verifier si les autres traitements ont marché
        """
        # Affichage des types de données après nettoyage
        print("Types de données après nettoyage :")
        print(self.client.dtypes)

    # Affichage des 10 premières lignes après nettoyage
        print("Les 10 premières lignes après nettoyage :")
        print(self.client.head(10))


    # Méthode pour afficher les boxplots

    def afficher_boxplots(self):
        """
        Affiche des boxplots pour chaque colonne numérique du DataFrame pour identifier s'il y'a des valeurs
         abérantes.
         """
        colonnes_numeriques = self.client.select_dtypes(include=['int32','float32','int64', 'float64']).columns.drop('ID Client')

        for colonne in colonnes_numeriques:
            plt.figure(figsize=(8, 6))
            plt.boxplot(self.client[colonne])
            plt.title(f'Boxplot de {colonne}')
            plt.xlabel(colonne)
            plt.ylabel('Valeurs')
            plt.show()

    # Méthodes pour explorer les données

    def explorer_donnees(self):
        """
        Effectue la phase d'exploration des données.

        Cette méthode analyse la durée de l'abonnement avant résiliation et examine les clients avec remise.
        """
        self.analyser_duree_abonnement()
        self.analyser_clients_remise()
        self.analyser_clients_sans_resiliation()
        self.afficher_boxplots()
        self.test_traitement_colonnes()
        self.analyse_cohorte()
       

    # Méthodes d'analyse des données

    def analyser_duree_abonnement(self):
        """
        Analyse la durée de l'abonnement avant résiliation.
        """
        clients_resilies = self.client[self.client['Resiliation'] == 1]
        clients_resilies['Durée Avant Resiliation'] = clients_resilies['Date Annulation'] - clients_resilies['Date Inscription']

        # Calcul de la durée moyenne avant résiliation
        duree_moyenne_resiliation = clients_resilies['Durée Avant Resiliation'].mean().days

        # Visualisation des données avec la durée moyenne
        plt.figure(figsize=(8, 6))
        plt.hist(clients_resilies['Durée Avant Resiliation'].dt.days, bins=20, color='skyblue', edgecolor='black')
        plt.axvline(duree_moyenne_resiliation, color='red', linestyle='dashed', linewidth=1, label=f'Durée moyenne: {round(duree_moyenne_resiliation, 2)} jours')
        plt.xlabel('Durée avant résiliation (jours)')
        plt.ylabel('Nombre de clients')
        plt.title('Distribution de la durée avant résiliation pour les clients ayant résilié')
        plt.legend()
        plt.grid(True)
        plt.show()


    def analyser_clients_remise(self):
        """
        Analyse des clients ayant résilié selon la présence de remise
        """
        nb_clients_resilies_avec_remise = len(self.client[(self.client['Resiliation'] == 1) & (self.client['Remise'] == 1)])
        nb_total_clients_resilies = len(self.client[self.client['Resiliation'] == 1])
        pourcentage_clients_resilies_avec_remise = (nb_clients_resilies_avec_remise / nb_total_clients_resilies) * 100

        # Affichage des résultats
        labels = ['Avec remise', 'Sans remise']
        sizes = [nb_clients_resilies_avec_remise, nb_total_clients_resilies - nb_clients_resilies_avec_remise]
        colors = ['lightcoral', 'lightskyblue']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Répartition des clients ayant résilié selon la présence de remise')
        plt.axis('equal')
        plt.show()

    def analyser_clients_sans_resiliation(self):
        """
        Analyse les clients n'ayant pas résilié leur abonnement.
        """
        clients_non_resilies = self.client[self.client['Resiliation'] == 0]
        nb_total_clients_non_resilies = len(clients_non_resilies)
        nb_clients_non_resilies_avec_remise = len(clients_non_resilies[clients_non_resilies['Remise'] == 1])

        # Calcul des pourcentages
        pourcentage_clients_non_resilies_avec_remise = (nb_clients_non_resilies_avec_remise / nb_total_clients_non_resilies) * 100
        pourcentage_clients_non_resilies_sans_remise = 100 - pourcentage_clients_non_resilies_avec_remise

        # Affichage des résultats
        labels = ['Avec remise', 'Sans remise']
        sizes = [pourcentage_clients_non_resilies_avec_remise, pourcentage_clients_non_resilies_sans_remise]
        colors = ['lightcoral', 'lightskyblue']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Répartition des clients sans résiliation selon la présence de remise')
        plt.axis('equal')
        plt.show()
    def analyse_cohorte(self):
        """
        Analyse de cohorte pour suivre les taux de résiliation au fil du temps.
        """

        # Création d'une cohorte basée sur la date d'inscription
        self.client['Cohorte'] = self.client['Date Inscription'].dt.to_period('M')

        # Groupement des clients par cohorte et calcul du taux de résiliation
        cohort_resiliation = self.client.groupby(['Cohorte', 'Remise'])['Resiliation'].mean().unstack()

        # Création du graphique
        cohort_resiliation.plot(figsize=(10, 6), marker='o')

        # Ajout de légendes et de titres
        plt.title('Analyse de cohorte des taux de résiliation en fonction de la présence de remise')
        plt.xlabel('Cohorte')
        plt.ylabel('Taux de résiliation moyen')
        plt.xticks(rotation=45)
        plt.legend(['Sans remise', 'Avec remise'])
        plt.grid(True)
        plt.show()



##--------------------------------------------HAOMING-------------------------------------------##



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
        print("Nombre de valeurs manquantes dans table service : \n", self.service.isnull().sum())
        print("Nombre de valeurs manquantes dans table information session login : \n", self.infoLogin.isnull().sum())
        print("Nombre de valeurs manquantes dans table historique service : \n", self.histService.isnull().sum())
        
        print("Nombre de lignes dupliquées dans table service : \n", self.service.duplicated().sum())
        print("Nombre de lignes dupliquées dans table information session login : \n", self.infoLogin.duplicated().sum())
        print("Nombre de lignes dupliquées dans table historique service : \n", self.histService.duplicated().sum())
        
        print("Nombre de plan d\'abonnement utilisés : \n", self.service['Type Service'].value_counts())
        print("Nombre de services utilisés : \n", self.histService['ID Service'].value_counts().sort_index())
        
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
        # Affichage des types de données après nettoyage
        print("Types de données après nettoyage :")
        print(self.service.dtypes)
        print(self.infoLogin.dtypes)
        print(self.histService.dtypes)

        # Conversion des valeurs de 'Date Inscription' en datetime, en gérant les valeurs déjà de type datetime.date
        self.data_historique['Date Inscription'] = self.data_historique['Date Inscription'].apply(lambda x: x if isinstance(x, pd.Timestamp) else pd.to_datetime(x))

        # Affichage des lignes aberrantes après nettoyage
        lig_aberrant_traitee = self.data_historique[self.data_historique['Date Heure'].dt.date < self.data_historique['Date Inscription']].reset_index()
        print("Nombre de lignes aberrantes après traitement : ", len(lig_aberrant_traitee))
    
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
        plt.title('Nombre de session dans différent année')
        plt.xlabel('Année')
        plt.ylabel('Nombre de session')
        plt.show()
        
  
        
  
###--------------------------------Lyse et Haoming-------------------------------------------##        
   


     
class DataModeling:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.df_modelisation = pd.DataFrame()

    def create_modeling_dataframe(self):
        # Ajouter les colonnes
        self.df_modelisation['ID Client'] = self.data_processor.client['ID Client']
        self.df_modelisation['Annulation'] = self.data_processor.client['Date Annulation'].notnull().astype(int)
        self.df_modelisation['Remise'] = self.data_processor.client['Remise'].apply(lambda x: 1 if x == 'Oui' else 0)

        # Calculer le nombre de sessions par client
        sessions_par_client = self.data_processor.data_historique.groupby('ID Client')['Date Heure'].count()
        self.df_modelisation = self.df_modelisation.merge(sessions_par_client, how='left', left_on='ID Client', right_index=True)
        self.df_modelisation.rename(columns={'Date Heure': 'Nombre Session'}, inplace=True)
        self.df_modelisation['Nombre Session'] = self.df_modelisation['Nombre Session'].fillna(0)

        # Calculer le pourcentage d'utilisation de chaque type de plan par client
        plans_par_client = self.data_processor.data_historique.groupby(['ID Client', 'Type Service'])['ID Service'].count().unstack(fill_value=0)
        plans_par_client = plans_par_client.div(plans_par_client.sum(axis=1), axis=0) * 100
        self.df_modelisation = self.df_modelisation.merge(plans_par_client, how='left', left_on='ID Client', right_index=True)
        self.df_modelisation.rename(columns={'Eco Basique': 'Pourcentage plan basique', 'Eco Confort': 'Pourcentage plan confort', 
                                              'Eco Premium':'Pourcentage plan premium'}, inplace=True)
        self.df_modelisation[['Pourcentage plan basique','Pourcentage plan confort','Pourcentage plan premium']] = self.df_modelisation[['Pourcentage plan basique', 'Pourcentage plan confort', 'Pourcentage plan premium']].fillna(0)

    def display_modeling_dataframe(self):
        print(self.df_modelisation.head())

        # Afficher les colonnes
        print(self.df_modelisation.columns)

        # Calculer la matrice de corrélation
        matrice_corr = self.df_modelisation.corr()

        # Afficher la matrice de corrélation
        print("Matrice de corrélation :")
        print(matrice_corr)
        

if __name__ == "__main__":
    # Création d'une instance de la classe  DataProcess
    data_processor = DataProcess('clients_greendwell.csv', 'historique_acces_greendwell.xlsx')
    # Appel de ses méthodes
    data_processor.nettoyer_donnees()
    data_processor.explorer_donnees()
    # Création d'une instance de la classe DataCleaningExploration
    data_processor1= DataCleaningExploration('clients_greendwell.csv')
    # Appel de ses méthodes
    data_processor1.collecte_donnees()
    data_processor1.nettoyer_donnees()
    data_processor1.explorer_donnees()
    # Création d'une instance de la classe DataModeling 
    data_modeling = DataModeling(data_processor)
    # Appel de ses méthodes
    data_modeling.create_modeling_dataframe()
    data_modeling.display_modeling_dataframe()

    
