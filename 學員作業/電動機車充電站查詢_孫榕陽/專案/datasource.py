
import sqlite3
import pandas as pd

# 1. 讀取 CSV 檔案
csv_file = './battery01.csv'  # 替換成你的 CSV 檔案路徑
df = pd.read_csv(csv_file)

# 2. 連接到 SQLite 資料庫（如果資料庫不存在，它會自動創建）
conn = sqlite3.connect('example.db')  # 替換成你的資料庫檔案
cursor = conn.cursor()

# 3. 創建資料表（如果需要的話），並設置唯一約束來防止重複資料
create_table_query = """
CREATE TABLE IF NOT EXISTS battery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    dist TEXT NOT NULL,
    sitename TEXT NOT NULL,
    address TEXT NOT NULL,
    lat TEXT NOT NULL,
    lon TEXT NOT NULL,
    UNIQUE(city, dist, sitename, address,lat,lon)  -- 設置唯一約束，確保資料不會重複
)
"""
cursor.execute(create_table_query)

# 4. 清空資料表，這樣我們可以避免任何舊資料的影響
# 如果你希望保留資料，可以跳過此步驟
cursor.execute("DELETE FROM battery")
conn.commit()

# 5. 遍歷 CSV 資料並插入資料庫
for index, row in df.iterrows():
    city = row['city']
    dist = row['dist']
    sitename = row['sitename']
    address = row['address']
    lat=row['lat']
    lon=row['lon']

    # 檢查資料是否完整
    if not all([city, dist, sitename, address,lat,lon]):
        print(f"跳過不完整的資料: {row}")
        continue  # 跳過不完整的項目

    # 插入資料之前，檢查資料是否已存在
    cursor.execute('''
        SELECT 1 FROM battery WHERE city=? AND dist=? AND sitename=? AND address=? AND lat=? AND lon=?
    ''', (city, dist, sitename, address, lat, lon))

    # 如果資料已經存在，則跳過插入
    if cursor.fetchone():
        print(f"資料已存在，跳過: {row}")
        continue

    # 插入資料庫
    sql = '''INSERT INTO battery(city, dist, sitename, address,lat,lon)
             VALUES (?, ?, ?, ?,?,?)'''
    cursor.execute(sql, (city, dist, sitename, address,lat,lon))

# 6. 提交並關閉連線
conn.commit()
conn.close()

print(f"資料已經成功從 '{csv_file}' 插入到資料庫中。")

#---------------------------------------------------------------------------------

def get_sitename(county:str)->list[str]:
    '''
    docString
    parameter:
        county:城市名稱
    return:
        傳出所有的站點名稱
    '''
    conn = sqlite3.connect("example.db")
    with conn:
        cursor = conn.cursor()
        sql = '''
        SELECT DISTINCT dist
        FROM battery
        WHERE city=?
        '''
        cursor.execute(sql,(county,))
        distnames = [items[0] for items in cursor.fetchall()]
    
    return distnames

def get_county()->list[str]:
    '''
    docString
    parameter:
    return:
        傳出所有的城市名稱
    '''
    conn = sqlite3.connect("example.db")
    with conn:
        cursor = conn.cursor()
        sql = '''
        SELECT DISTINCT city
        FROM battery
        '''
        cursor.execute(sql)
        counties = [items[0] for items in cursor.fetchall()]
    
    return counties

def get_selected_data(city:str, dist:str)->list[list]:
    '''
    使用者選擇了 sitename, 並將 sitename 傳入
    Parameter:
        sitename: 站點的名稱
    Return:
        所有關於此站點的相關資料
    '''
    conn = sqlite3.connect("example.db")
    with conn:
        cursor = conn.cursor()
        sql = '''
        SELECT city, dist, sitename, address,lat,lon
        FROM battery
        WHERE city=? AND dist=?
        '''
        cursor.execute(sql, (city, dist))
        sitename_list = [list(item) for item in cursor.fetchall()]
    
    return sitename_list

def download_data():
    conn = sqlite3.connect("example.db")

    try:
        # 假設 CSV 檔案的路徑是 "battery.csv"
        csv_file = 'battery01.csv'  # 請替換成你的 CSV 檔案路徑
        df = pd.read_csv(csv_file)

    except FileNotFoundError as e:
        print(f"檔案未找到: {e}")
        return
    except pd.errors.EmptyDataError as e:
        print(f"CSV 檔案為空: {e}")
        return
    except Exception as e:
        print(f"讀取 CSV 發生錯誤: {e}")
        return
    else:
        # 假設 CSV 檔案有 'sitename', 'city', 'dist', 'address' 'lat' ,'lon'等欄位
        with conn:
            cursor = conn.cursor()

            for index, row in df.iterrows():
                city = row['city']
                dist = row['dist']
                sitename = row['sitename']
                address = row['address']
                lat=row['lat']
                lon=row['lon']

                # 檢查資料是否完整
                if not all([city, dist, sitename, address,lat,lon]):
                    print(f"跳過不完整的資料: {row}")
                    continue  # 跳過不完整的項目

                # 插入資料庫，這裡仍然使用 'INSERT OR IGNORE' 來處理已存在的資料
                sql = '''INSERT OR IGNORE INTO battery(city, dist, sitename, address,lat,lon)
                         VALUES (?, ?, ?, ?,?,?)'''
                cursor.execute(sql, (city, dist, sitename, address,lat,lon))

        print("資料已成功下載並插入資料庫。")