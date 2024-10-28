import requests
def get_sitename()->list[str]:
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_488?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(e)
    else:
        sitenames = set()
        for items in data['records']:
            sitenames.add(items['sitename'])

        sitenames = list(sitenames)
        return sitenames
    
def get_selected_data(sitename:str)->list[list]:
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_488?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(e)
    else:
        outerlist = []
        for items in data['records']:
            if items['sitename'] == sitename:
                innerlist = [items['datacreationdate'],items['county'],items['aqi'],items['pm2.5'],items['status'],items['latitude'],items['longitude']]
                outerlist.append(innerlist)

            
        return outerlist