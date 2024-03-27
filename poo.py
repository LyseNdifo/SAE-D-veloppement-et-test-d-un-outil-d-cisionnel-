import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

   





    
#Execution de nos méthodes

if __name__ == "__main__":
    data_processor = DataCleaningExploration('clients_greendwell.csv')
    data_processor.collecte_donnees()
    data_processor.nettoyer_donnees()
    data_processor.explorer_donnees()
