import pandas as pd
import sqlite3

class PetDataSource:
    def __init__(self):
        self.df = pd.read_csv('2024-2014pet_data.csv')
        self._create_database()

    def _create_database(self):
        """Create SQLite database from CSV data"""
        conn = sqlite3.connect("pet_data.db")
        with conn:
            self.df.to_sql('pet_records', conn, if_exists='replace', index=False)
        
    def get_years(self) -> list[str]:
        """Get list of available years"""
        conn = sqlite3.connect("pet_data.db")
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT Year FROM pet_records ORDER BY Year DESC')
            years = [str(item[0]) for item in cursor.fetchall()]
        return years

    def get_counties(self) -> list[str]:
        """Get list of available counties with specified order"""
        county_order = [
            "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", 
            "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市",
            "嘉義縣", "臺南市", "高雄市", "屏東縣", "臺東縣", "花蓮縣",
            "宜蘭縣", "澎湖縣", "金門縣", "連江縣"
        ]
        
        # 取得實際存在於資料中的縣市
        conn = sqlite3.connect("pet_data.db")
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT County FROM pet_records WHERE County != "全臺"')
            available_counties = set(item[0] for item in cursor.fetchall())
        
        # 只回傳實際存在於資料中的縣市，並保持指定順序
        ordered_counties = [county for county in county_order if county in available_counties]
        return ordered_counties

    def get_county_data(self, county: str) -> list[list]:
        """Get data for a specific county across all years"""
        conn = sqlite3.connect("pet_data.db")
        with conn:
            cursor = conn.cursor()
            sql = '''
            SELECT Year, County, Registrations, Deregistrations, Neutered, "Neutering Rate"
            FROM pet_records
            WHERE County = ?
            ORDER BY Year DESC
            '''
            cursor.execute(sql, (county,))
            data = [list(item) for item in cursor.fetchall()]
        return data