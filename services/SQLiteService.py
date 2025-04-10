import os
import sys
from pathlib import Path

class SQLiteService:
    def __init__(self, db_path=None):
        # Détermination dynamique de la racine du projet
        if db_path is None:
            # Cas 1 : Exécution dans un script (__file__ existe)
            if hasattr(sys, 'frozen'):  # Application compilée (ex: PyInstaller)
                root_dir = Path(sys.executable).parent
            elif '__file__' in globals():
                root_dir = Path(__file__).resolve().parent.parent
            # Cas 2 : Exécution dans un notebook Jupyter
            else:
                # Stratégie de repli : remonter depuis le répertoire courant
                current_dir = Path(os.getcwd())
                # Logique pour identifier la racine du projet
                if (current_dir / 'data').exists():
                    root_dir = current_dir
                else:
                    root_dir = current_dir.parent  # Ajuster selon la structure

            self.db_path = root_dir / "data" / "weather_data.db"
        else:
            self.db_path = Path(db_path).resolve()

        # Création garantie du répertoire parent
        self.db_path.parent.mkdir(parents=True, exist_ok=True)        
        self.connection = None

    def connect(self):
        import sqlite3
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # [6][10]
        return self


    def close(self):
        if self.connection:
            self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Weather (
                datetime TEXT PRIMARY KEY,
                temperature REAL NOT NULL
            );
            ''')

        self.connection.commit()
    
    def insert_data(self, data):
        cursor = self.connection.cursor()
        cursor.executemany(
            "INSERT OR REPLACE INTO Weather (datetime, temperature) VALUES (?, ?)",
            data
        )
        self.connection.commit()
    
    def select_data(self):
        """Retourne les données météo sous forme de dictionnaires"""
        try:
            cursor = self.connection.cursor()
            
            # Exécution de la requête avec vérification
            cursor.execute("SELECT * FROM Weather")  # Correction de la table [1]
            
            # Récupération des métadonnées des colonnes
            columns = [desc[0] for desc in cursor.description]  # [3][5][10]
            
            # Construction des résultats
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))  # [6][10]
                
            return results
            
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données : {e}")
            raise
        finally:
            cursor.close()  # Fermeture systématique [3][7]