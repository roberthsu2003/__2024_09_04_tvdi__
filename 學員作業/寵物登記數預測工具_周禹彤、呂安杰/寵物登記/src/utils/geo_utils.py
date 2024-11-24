import pandas as pd
import sqlite3
from typing import List, Tuple, Dict, Optional

class PetDataManager:
    """統一的寵物資料管理類別"""
    def __init__(self, csv_file: str = '2023-2009pet_data.csv'):
        """
        初始化資料管理器
        
        Args:
            csv_file: CSV 資料檔案路徑
        """
        self.df = pd.read_csv(csv_file)
        self._initialize_database()
        self._county_order = [
            "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", 
            "苗栗縣", "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市",
            "嘉義縣", "臺南市", "高雄市", "屏東縣", "臺東縣", "花蓮縣",
            "宜蘭縣", "澎湖縣", "金門縣", "連江縣"
        ]

    def _initialize_database(self):
        """初始化 SQLite 資料庫"""
        self.conn = sqlite3.connect(":memory:")
        self.df[self.df['County'] != '全臺'].to_sql(
            'pet_records', 
            self.conn, 
            if_exists='replace', 
            index=False
        )

    def get_years(self) -> List[str]:
        """取得所有年份列表"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT DISTINCT Year FROM pet_records ORDER BY Year DESC')
        return [str(year[0]) for year in cursor.fetchall()]

    def get_counties(self) -> List[str]:
        """取得所有縣市列表（依指定順序）"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT DISTINCT County FROM pet_records')
        available_counties = set(county[0] for county in cursor.fetchall())
        return [county for county in self._county_order if county in available_counties]

    def get_county_data(self, county: str) -> List[Tuple]:
        """
        取得特定縣市的所有資料
        
        Args:
            county: 縣市名稱
            
        Returns:
            List[Tuple]: 該縣市的所有年度資料
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT Year, County, Registrations, Deregistrations, 
                   Neutered, "Neutering Rate"
            FROM pet_records
            WHERE County = ?
            ORDER BY Year DESC
        ''', (county,))
        return cursor.fetchall()

    def get_yearly_summary(self, year: int) -> Dict[str, float]:
        """
        取得特定年份的統計摘要
        
        Args:
            year: 年份
            
        Returns:
            Dict[str, float]: 包含各項統計數據的字典
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                SUM(Registrations) as total_reg,
                SUM(Deregistrations) as total_dereg,
                SUM(Neutered) as total_neutered,
                AVG("Neutering Rate") as avg_rate
            FROM pet_records
            WHERE Year = ?
        ''', (year,))
        return dict(zip(
            ['total_reg', 'total_dereg', 'total_neutered', 'avg_rate'],
            cursor.fetchone()
        ))

    def __del__(self):
        """清理資源"""
        if hasattr(self, 'conn'):
            self.conn.close()