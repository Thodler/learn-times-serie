class OpenMeteoService:
    def __init__(self, atDateStart="2025-01-01", latitude=52.52, longitude=13.41):
        self._url = "https://archive-api.open-meteo.com/v1/era5"
        self._params = (
            f"?latitude={latitude}&longitude={longitude}&start_date={atDateStart}&end_date=2025-02-02&hourly=temperature_2m"
        )

    def get_url(self):
        return self._url + self._params
    
    def get_data(self):
        import requests

        print(self.get_url())
        response = requests.get(self.get_url())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")