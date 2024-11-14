# datasource.py

import random
from datetime import datetime, timedelta
import pandas as pd
import sqlite3

# Function to get the start date of a specific week in a given year
def get_week_start(year, week):
    return datetime.strptime(f'{year}-W{str(week).zfill(2)}-1', "%Y-W%W-%w")

# Function to generate order data
def generate_orders():
    order_ids = [f'2024-{str(i).zfill(2)}' for i in range(1, 51)]
    orders = []
    
    for order_id in order_ids:
        order_week = int(order_id.split('-')[1])
        order_week_start = get_week_start(2024, order_week)
        
        # Generate random order and delivery dates
        order_date = order_week_start - timedelta(weeks=random.choice([1, 2]), days=random.randint(0, 6))
        delivery_date = order_week_start + timedelta(weeks=random.choice([4, 5]), days=random.randint(0, 6))
        factory = random.choice(['China', 'Vietnam'])
        
        orders.append({
            'Order ID': order_id,
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Delivery Date': delivery_date.strftime('%Y-%m-%d'),
            'Factory': factory
        })
    return orders

# Function to generate sales data
def generate_sales_orders(orders):
    sales_ids = ['Sales A', 'Sales B', 'Sales C', 'Sales D', 'Sales E']
    sales_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
    customers = [f'Customer {i}' for i in range(1, 21)]
    
    data = []
    
    for sales_id, sales_name in zip(sales_ids, sales_names):
        assigned_customers = random.sample(customers, k=5)
        for customer in assigned_customers:
            num_orders = random.randint(3, 4)
            for _ in range(num_orders):
                order_id = random.choice([order['Order ID'] for order in orders])
                yield_rate = round(random.uniform(96.1, 99.8), 2)
                thru_put = round(random.uniform(950, 1200), 2)
                
                # Find the matching order details
                order_details = next((order for order in orders if order['Order ID'] == order_id), None)
                
                if order_details:
                    data.append([
                        sales_id, 
                        sales_name, 
                        customer, 
                        order_id, 
                        yield_rate, 
                        thru_put, 
                        order_details['Order Date'], 
                        order_details['Delivery Date'], 
                        order_details['Factory']
                    ])
    return data

# Function to save data to CSV
def save_to_csv(data, filename='sales_orders.csv'):
    columns = ['Sales ID', 'Sales Name', 'Customer ID', 'Order ID', 'Yield Rate', 
               'Thru_put', 'Order Date', 'Delivery Date', 'Factory']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False)
    print(f"CSV file '{filename}' has been created successfully.")
    return df

# Function to save data to SQLite database
def save_to_sqlite(df, db_filename='salesorders.db'):
    conn = sqlite3.connect(db_filename)
    table_name = 'sales_orders'
    
    # Create the table
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    create_table_query = f'''
    CREATE TABLE {table_name} (
        "Sales ID" TEXT,
        "Sales Name" TEXT,
        "Customer ID" TEXT,
        "Order ID" TEXT,
        "Yield Rate" REAL,
        "Thru_put" REAL,
        "Order Date" TEXT,
        "Delivery Date" TEXT,
        "Factory" TEXT
    )
    '''
    conn.execute(create_table_query)
    
    # Insert data into SQLite
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    print(f"Data has been successfully imported into '{db_filename}' database, table '{table_name}'.")

# Function to load data from SQLite database
def load_from_sqlite(db_filename='salesorders.db', table_name='sales_orders'):
    conn = sqlite3.connect(db_filename)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
