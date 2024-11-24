# datasource.py

from ast import Name
import random
from datetime import datetime, timedelta
import pandas as pd
import sqlite3

# get all sales names from database
def get_sales() -> list[str]:
    '''
    docString
    parameter:
    return:
        傳出所有業務的名字
    '''
    try:
        conn = sqlite3.connect("sales_orders.db")
        with conn:
            # Create a cursor object to execute SQL commands
            cursor = conn.cursor()
            
            # SQL query to select unique sales from sales_orders table
            sql = '''
            SELECT DISTINCT "sales_name"
            FROM sales_orders
            '''
            
            # Execute the SQL query
            cursor.execute(sql)
            
            # Get all results and extract the first item from each row into a list
            sales = [items[0] for items in cursor.fetchall()]
            
            # Print out the fetched sales names to confirm
            if sales:
                print("Sales Names:", sales)
            else:
                print("No sales names found in the database.")
                
        # Return the list of unique sales
        return sales

    except Exception as e:
        print("Error occurred:", e)
        return []

# Test the function
sales_list = get_sales()
print("Returned Sales List:", sales_list)


# Get the customer id-------------------
def get_customer_id(sales:str)->list[str]:
    '''
    docString
    parameter:
        sales:業務名稱

    return:
        傳出所有的客戶id
    '''
    conn = sqlite3.connect("sales_orders.db")
    with conn:
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # SQL query to select unique sitenames from records table
        sql = '''
        SELECT DISTINCT customer_id
        FROM sales_orders
        WHERE sales_name = ?
         '''
        # Execute the SQL query
        cursor.execute(sql, (sales, ))
        customer_id = [items[0] for items in cursor.fetchall()]
        
    # Debug print to confirm correct output
    print(f"Debug: Retrieved customer IDs for sales name '{sales}': {customer_id}")

    # Return the list of unique sitenames
    return customer_id


# def get_customers_by_sales_id(sales_id: str) -> list[str]:
#     conn = sqlite3.connect("sales_orders.db")
#     with conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT DISTINCT customer_id FROM sales_orders WHERE sales_id = ?", (sales_id,))
#         customers = [row[0] for row in cursor.fetchall()]
#     return customers