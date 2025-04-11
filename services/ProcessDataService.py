from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

class ProcessDataService:
    def __init__(self, dataset):
        self.dataset_origin = dataset
        self.dataset = dataset

    def view_stationarity(self):
        # Calculer la moyenne mobile et l'écart-type mobile
        rolling_mean = self.dataset.rolling(window=12).mean()
        rolling_std = self.dataset.rolling(window=12).std()

        # Tracer les données

        plt.figure(figsize=(12, 6))
        plt.plot(self.dataset, label='Données originales', color='blue')
        plt.plot(rolling_mean, label='Moyenne mobile', color='red')
        plt.plot(rolling_std, label='Écart-type mobile', color='green')
        plt.legend(loc='best')
        plt.title('Stationnarité des données')
        plt.show()

        return self

    def adf_test(self):

        result = adfuller(self.dataset)
        # Afficher les résultats
        print("Statistique de test ADF:", result[0])
        print("p-value:", result[1])
        print("Nombre de retards utilisés:", result[2])
        print("Nombre d'observations:", result[3])
        print("Valeurs critiques:")
        for key, value in result[4].items():
            print(f"   {key}: {value}")

        # Interprétation
        if result[1] < 0.05:
            print("La série est stationnaire (p-value < 0.05).")
        else:
            print("La série n'est pas stationnaire (p-value >= 0.05).")
        
        return self

    def reset_dataset(self):
        self.dataset = self.dataset_origin.copy()
        return self