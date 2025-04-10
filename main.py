from services.OpenMeteoService import OpenMeteoService
from services.SQLiteService import SQLiteService

# Recupérationde l'API
print("Récupération des données de l'API...")
api = OpenMeteoService()
data = api.get_data()
print("Données récupérées avec succès !")

print("Extraction des données...")
# Combiner les valeurs de temps et de température dans une liste de tuples
extracted_data = list(zip(data['hourly']['time'], data['hourly']['temperature_2m']))
print("Données extraites avec succès !")

print("Création de la base de données...")
db = SQLiteService()
db.connect()
print("Connexion à la base de données réussie !")
print("Création de la table...")
db.create_table()
print("Table créée avec succès !")
print("Insertion des données dans la base de données...")
db.insert_data(extracted_data)
print("Base de données créée avec succès !")