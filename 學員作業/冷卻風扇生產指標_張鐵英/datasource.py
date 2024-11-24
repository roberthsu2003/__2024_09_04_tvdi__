# datasource.py

from ast import Name
import random
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
from pandas import DataFrame

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
            # if sales:
            #     print("Sales Names:", sales)
            # else:
            #     print("No sales names found in the database.")
                
        # Return the list of unique sales
        return sales

    except Exception as e:
        print("Error occurred:", e)
        return []

# Test the function
sales_list = get_sales()
# print("Returned Sales List:", sales_list)


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

def get_selected_data(customer_id: str) -> list[list]:
    conn = sqlite3.connect("sales_orders.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_date, deliver_date, customer_id, order_id, yield_rate, thru_put, factory
            FROM sales_orders WHERE customer_id = ?
            ORDER BY order_date DESC
        """, (customer_id,))
        return [list(row) for row in cursor.fetchall()]
    
def get_plot_data(customer_id: str) -> DataFrame:
    conn = sqlite3.connect("sales_orders.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_date, yield_rate, thru_put FROM sales_orders WHERE customer_id = ?
        """, (customer_id,))
        rows = cursor.fetchall()

    # Check if rows are returned
    if not rows:
        raise ValueError(f"No data found for customer_id: {customer_id}")

    # Convert rows to DataFrame
    data = [{'order_date': row[0], 'yield_rate': row[1], 'thru_put': row[2]} for row in rows]
    df = pd.DataFrame(data)

    # Ensure the DataFrame has the expected structure
    if 'order_date' not in df.columns:
        raise KeyError("The 'order_date' column is missing in the DataFrame.")

    # Convert order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df.set_index('order_date')  # Set order_date as the index

