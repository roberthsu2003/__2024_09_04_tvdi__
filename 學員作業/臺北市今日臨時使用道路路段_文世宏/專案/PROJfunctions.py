from pyproj import Transformer
from geopy.geocoders import Nominatim
import requests
from requests import Response
import sqlite3
import time
from pyproj import Proj, transform

############################得到今天資料#########################################
url = "https://tpnco.blob.core.windows.net/blobfs/Rally/TodayUrgentCase.json"
try:
    response:Response = requests.get(url)
    response_json = response.json()
    data = response.json()
    print(response.text)
except Exception as e:
    print(e)
#########################################################################

#########################################################################
'''得到資料裡面的coordinates 第0個欄位是座標屬於的資料'''
result = []

# 遍歷 features 中的每個 JSON 物件
for feature in data["features"]:
    # 提取該 feature 的 geometry["0"] 中的所有座標
    coordinates_list = feature["geometry"]["coordinates"][0]
    
#     # 提取該 feature 的 BILL_CODE
    bill_code = feature["properties"]["BILL_CODE"]
    
    # # 遍歷每個座標，將 BILL_CODE 和座標結合，並加入結果列表
    for coordinates in coordinates_list:
        result.append([bill_code] + coordinates)

# 顯示結果
print(result)
#########################################################

##########################################################
'''得到字典{billcode:[x,y],billcode:[x,y]}'''
coordinates_dict = {}

for item in result:
    # 取出每筆資料的編號（例如 '10967113574169'）
    identifier = item[0]
    # 取得對應的坐標資料 (x, y)
    coordinates = [item[1], item[2]]
    
    # 如果這個編號已經在字典裡，則將新的坐標資料加到現有的列表中
    if identifier not in coordinates_dict:
        coordinates_dict[identifier] = []  # 如果該編號還沒有資料，創建一個空列表
    coordinates_dict[identifier].append(coordinates)

print(coordinates_dict)

###############################################################################
'''轉換xy變成經緯度'''
# 定義 TWD97 和 WGS84 座標系統
twd97 = Proj(init='epsg:3826')  # TWD97
wgs84 = Proj(init='epsg:4326')  # WGS84

# 假設有多筆 TWD97 坐標 [[x1, y1], [x2, y2], ...]
coordinates_twd97 = coordinates_dict['10967113574169']

# 轉換所有 TWD97 坐標為 WGS84
coordinates_wgs84 = []
# for i in coordinates_dict:
#     coordinates_twd97 = coordinates_dict[i]
for x, y in coordinates_twd97:
    # 轉換為 WGS84 坐標
    longitude, latitude = transform(twd97, wgs84, x, y)
    coordinates_wgs84.append([longitude, latitude])

##########################################################

conn = sqlite3.connect('TPEroad.db')
sql = '''
INSERT INTO coordinates_test
(BILL_CODE, x, y)
VALUES(?, ?, ?);
'''

