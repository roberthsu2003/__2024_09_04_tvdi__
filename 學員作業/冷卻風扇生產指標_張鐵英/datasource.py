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
            
        return sales

    except Exception as e:
        print("Error occurred:", e)
        return []

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


# def get_selected_data(customer_id: str) -> list[list]:
#     # Debugging: Print the input customer_id
#     print(f"get_selected_data called with customer_id: {customer_id}")

#     conn = sqlite3.connect("sales_orders.db")
#     with conn:
#         cursor = conn.cursor()
#         sql = """
#             SELECT sales_id, sales_name, customer_id, order_id, yield_rate, thru_put, order_date, deliver_date, factory
#             FROM sales_orders WHERE customer_id = ?
#             ORDER BY order_date DESC
#         """
#         try:
#             cursor.execute(sql, (customer_id,))
#             customer_list = [list(row) for row in cursor.fetchall()]
#             # Debugging: Print the fetched customer list
#             print(f"Fetched customer_list: {customer_list}")
#             return customer_list
#         except sqlite3.ProgrammingError as e:
#             # Debugging: Print detailed error information
#             print(f"SQLite ProgrammingError: {e}")
#             raise

#------------------------------------------------------------
def get_selected_data(customer_id: str, sales_id: str) -> list[list]:
    # Normalize inputs (trim whitespace and normalize case)
    customer_id = customer_id.strip()
    sales_id = sales_id.strip()

    print(f"#1 -- get_selected_data called with customer_id: {customer_id}, sales_id: {sales_id}")  # Debugging

    conn = sqlite3.connect("sales_orders.db")
    with conn:
        cursor = conn.cursor()
        sql = """
            SELECT sales_id, sales_name, customer_id, order_id, yield_rate, thru_put, order_date, deliver_date, factory
            FROM sales_orders
            WHERE customer_id = ? AND sales_id = ?
            ORDER BY order_date DESC
        """
        try:
            cursor.execute(sql, (customer_id, sales_id))  # Pass both parameters
            customer_list = [list(row) for row in cursor.fetchall()]
            print(f"#2 -- Fetched data for customer_id {customer_id} under sales_id {sales_id}: {customer_list}")  # Debugging
            return customer_list
        except sqlite3.ProgrammingError as e:
            print(f"SQLite ProgrammingError: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in get_selected_data: {e}")
            raise


def debug_sales_customer_pairs():
    conn = sqlite3.connect("sales_orders.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT sales_id, customer_id FROM sales_orders")
        pairs = cursor.fetchall()
        print("# Debugging -- Sales-Customer Pairs in Database:")
        for pair in pairs:
            print(pair)
#------------------------------------------------------------------------
    
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

