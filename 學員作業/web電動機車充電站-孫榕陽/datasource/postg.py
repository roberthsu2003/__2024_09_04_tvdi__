import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

def get_cities()->list[dict]:
    with psycopg2.connect(database=os.environ['Postgres_DB'],
                      user=os.environ['Postgres_user'],
                      host=os.environ['Postgres_HOST'],
                      password=os.environ['Postgres_password']) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM city')
            data:list[tuple] = cursor.fetchall()
    
#list comprehension

    convert_data:list[dict] = [{'_id':item[0],
                                'city_name':item[1],
                                'continent':item[2],
                                'country':item[3],
                                'image':item[4]
                                } for item in data]
    return convert_data

def is_email_duplicate(email:str) -> bool:
    with psycopg2.connect(database=os.environ['Postgres_DB'],
                      user=os.environ['Postgres_user'],
                      host=os.environ['Postgres_HOST'],
                      password=os.environ['Postgres_password']) as conn:
        with conn.cursor() as cursor:
            sql = '''
                SELECT count(*) 
                FROM  public.user
                WHERE user_email = %s;
            '''
            cursor.execute(sql,(email,))
            nums:tuple = cursor.fetchone()
            return False if nums[0]==0 else True
        
def add_user(name:str, email:str, password:str) -> bool:
    with psycopg2.connect(database=os.environ['Postgres_DB'],
                      user=os.environ['Postgres_user'],
                      host=os.environ['Postgres_HOST'],
                      password=os.environ['Postgres_password']) as conn:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO public.USER(user_name,user_email,password)
                VALUES (%s,%s,%s); 
            '''
            try:
                cursor.execute(sql,(name,email,password))
            except Exception:
                return False
            return True
            
            