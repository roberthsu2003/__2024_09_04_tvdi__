import pandas as pd

class DataManager:
    def __init__(self):
        self._load_pet_data()

    def _load_pet_data(self):
        df = pd.read_csv('2024-2014pet_data.csv')
        df = df[df['County'] != '全臺']
        
        self.pet_data = {}
        for county in df['County'].unique():
            county_data = df[df['County'] == county]
            self.pet_data[county] = [
                (row['Year'], row['County'], row['Registrations'], 
                 row['Deregistrations'], row['Neutered'], row['Neutering Rate'])
                for _, row in county_data.iterrows()
            ]

    def get_counties(self):
        return list(self.pet_data.keys())

    def get_pet_data(self, county: str):
        return self.pet_data.get(county, [])