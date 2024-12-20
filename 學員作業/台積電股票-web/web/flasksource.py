import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
def get_cities()->list[dict]:
    with psycopg2.connect(database=os.environ['Postgres_DB'],
                        user=os.environ['Postgres_user'],
                        host =os.environ['Postgres_Host'],
                        password=os.environ['Postgres_password']) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM city')
            data = cursor.fetchall()
        
    #list comprehesion

    transfer_data:list[dict] = [{'_id':item[0],
                                'city_name':item[1],
                                'continent':item[2],
                                'country':item[3],
                                'image':item[4]
                                } for item in data]
    return transfer_data