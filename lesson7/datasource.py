import requests
import sqlite3
def get_sitename(county:str)->list[str]:
    '''
    docString
    parameter:
        county:城市名稱

    return:
        傳出所有的站點名稱
    '''
    conn = sqlite3.connect("AQI.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT sitename
        FROM records
        WHERE county = ?       
         '''
        # Execute the SQL query
        cursor.execute(sql,(county,))       
        sitenames = [items[0] for items in cursor.fetchall()]
        
    
    # Return the list of unique sitenames
    return sitenames

def get_county()->list[str]:
    '''
    docString
    parameter:
    return:
        傳出所有的城市名稱
    '''
    conn = sqlite3.connect("AQI.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT county
        FROM records
        '''
        # Execute the SQL query
        cursor.execute(sql)
        # Get all results and extract first item from each row into a list
        counties = [items[0] for items in cursor.fetchall()]
    
    # Return the list of unique sitenames
    return counties
    
def get_selected_data(sitename:str)->list[list]:
    '''
    使用者選擇了sitename,並將sitename傳入
    Parameter:
        sitename: 站點的名稱
    Return:
        所有關於此站點的相關資料
    '''
    conn = sqlite3.connect("AQI.db")
    with conn:
        cursor = conn.cursor()        
        sql = '''
        SELECT date,county,aqi,pm25,status,lat,lon
        FROM records
        WHERE sitename=?
        ORDER BY date DESC;
        '''
        cursor.execute(sql,(sitename,))
        sitename_list = [list(item) for item in cursor.fetchall()]
        return sitename_list
    
def download_data():
    conn = sqlite3.connect("AQI.db")
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_488?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(e)
    else:
        sitenames = set()
        with conn:
            cursor = conn.cursor()
            for items in data['records']:
                sitename = items['sitename']
                county = items['county']
                aqi = int(items['aqi']) if items['aqi'] != '' else 0
                status = items['status']
                pm25 = float(items['pm2.5']) if items['pm2.5'] != '' else 0.0
                date = items['datacreationdate']
                lon = float(items['longitude']) if items['longitude'] != '' else 0.0
                lat = float(items['latitude']) if items['latitude'] != '' else 0.0
                sql = '''INSERT OR IGNORE INTO records(sitename,county,aqi,status,pm25,date,lat,lon)
                        values (?,?, ?, ?,?,?,?,?);
                '''
                cursor.execute(sql,(sitename, county, aqi, status,pm25,date,lat,lon))