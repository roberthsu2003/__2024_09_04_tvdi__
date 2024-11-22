from pyproj import Transformer
from geopy.geocoders import Nominatim
import sqlite3


def xytransform(twx1:float,twy1:float):
    """
    把台灣座標x1y1轉換成世界座標
    """
    # 創建轉換器
    transformer = Transformer.from_crs("epsg:3826", "epsg:4326")
    twd97_x = twx1
    twd97_y = twy1
    # 轉換 TWD97 到 WGS84
    latitude,longitude = transformer.transform(twd97_x, twd97_y)

    print(f'2.TWD97轉WGS84: Latitude: {latitude:.7}, Longitude: {longitude:.7}')
    return latitude, longitude


def get_address_from_coordinates(lat, lon):
    """ 根據經緯度獲取地址或道路名稱 """
    # 初始化 Nominatim 反向地理編碼器
    geolocator = Nominatim(user_agent='PROJ')
    location = geolocator.reverse((lat, lon), language='zh-TW', exactly_one=True)
    if location:
        return location.address
    return "未找到地址"


def reverseaddress(location,alllist:list = None):
    """把取得的地址反轉成台北市在前"""
    list = alllist
    list_address = [item.strip() for item in location.split(",")]
    list_address.reverse()
    print(f'3.單次轉換結果{list_address}')
    list.append(list_address)
    print(f'4.總清單:{list}')
    return list_address




def latlonturn(mode,list:list = None,x = None,y = None) -> str:
    """
    參數 mode 必須是 'reverse' 或 'observe'。
    從台灣座標x1y1轉換成地址並拆開成 台灣 000 台北市 XXX XX區
    """
    valid_modes = ["reverse", "observe"]
    if mode not in valid_modes:
        raise ValueError(f"無效的模式：{mode}。可接受的模式有：{', '.join(valid_modes)}")

    if mode == "reverse":
        print("1.執行反轉操作")
        latitude, longitude = xytransform(x,y)
        location = get_address_from_coordinates(latitude, longitude)
        address = reverseaddress(location,list)
        return address
    elif mode == "observe":
        print("執行順序操作 沒有這個部分")


def get_district()->list[str]:
    '''
    docString
    parameter:
    return:
        傳出所有的行政區名稱
    '''
    conn = sqlite3.connect("TPEroad.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT 行政區
        FROM records
        '''
        # Execute the SQL query
        cursor.execute(sql)
        # Get all results and extract first item from each row into a list
        district = [items[0] for items in cursor.fetchall()]
    
    # Return the list of unique sitenames
    return district

def get_rodename(district:str)->list[str]:
    '''
    docString
    parameter:
        county:行政區名稱

    return:
        傳出行政區內所有登記的路段
    '''
    conn = sqlite3.connect("TPEroad.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT 新地址
        FROM records
        WHERE district = ?       
         '''
        # Execute the SQL query
        cursor.execute(sql,(district,))       
        full_address = [items[0] for items in cursor.fetchall()]
        
    
    # Return the list of unique sitenames
    return full_address

def get_selected_data(district:str)->list[list]:
    '''
    使用者選擇了disritct,並將district傳入
    Parameter:
        district: 站點的名稱
    Return:
        所有關於此站點的相關資料
    '''
    conn = sqlite3.connect("TPEroad.db")
    with conn:
        cursor = conn.cursor()        
        sql = '''
        SELECT 日期,
        新地址,
	    PRINTF("%.4f", ROUND(lat, 4)) AS Lat ,
        PRINTF("%.4f", ROUND(lon, 4)) as Lon 
        FROM records
        WHERE 行政區=?
        ORDER BY RCVdate DESC;
        '''
        cursor.execute(sql,(district,))
        address_list = [list(item) for item in cursor.fetchall()]
        return address_list