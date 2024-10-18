import requests
from requests import Response



def main():
    url_csv = 'https://data.moi.gov.tw/MoiOD/System/DoVwnloadFile.aspx?DATA=5481753E-52AF-40DA-9A8A-9E192B245E13'    

    try:
        res:Response = requests.request("GET",url_csv)
        res.raise_for_status()        
        res.encoding = 'utf-8'
        content:str = res.text
        with open('a1.csv',newline='',encoding='utf-8',mode='w') as file:
            print(type(file))
            file.write(content)
    except Exception as e:
            print(e)
    else:
         print("下載,儲存檔成功")
    

if __name__ == '__main__':
    main()