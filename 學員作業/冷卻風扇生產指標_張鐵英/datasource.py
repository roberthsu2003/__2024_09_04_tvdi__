# datasource.py

from ast import Name
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

# Function to save data to SQLite database one by one
def save_to_sqlite(df, db_filename='sales_orders1.db'):
    print("Saving data to SQLite database record by record...")
    conn = sqlite3.connect(db_filename)
    table_name = 'sales_orders1'

    # Create the table with an auto-incrementing 'id' field
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # Insert data into SQLite record by record
    cursor = conn.cursor()
    item = 1  # Initialize item counter
    
    for _, row in df.iterrows():
        sales_id = row['Sales ID']
        sales_name = row['Sales Name']
        customer_id = row['Customer ID']
        order_id = row['Order ID']
        yield_rate = float(row['Yield Rate']) if row['Yield Rate'] != '' else 0.0
        thru_put = float(row['Thru_put']) if row['Thru_put'] != '' else 0.0
        order_date = row['Order Date']
        delivery_date = row['Delivery Date']
        factory = row['Factory']

        # Insert each record one by one
        sql = f'''
        INSERT INTO {table_name} 
        ("Sales ID", "Sales Name", "Customer ID", "Order ID", "Yield Rate", "Thru_put", "Order Date", "Delivery Date", "Factory")
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (sales_id, sales_name, customer_id, order_id, yield_rate, thru_put, order_date, delivery_date, factory))
        print(f"Inserted item {item}: {sales_id}, {sales_name}, {customer_id}, {order_id}")
        item += 1
    
    conn.commit()
    conn.close()
    print(f"Data has been successfully imported into '{db_filename}' database, table '{table_name}'.")

# Function to load data from SQLite database
def load_from_sqlite(db_filename='sales_orders1.db', table_name='sales_orders1'):
    conn = sqlite3.connect(db_filename)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"Data has been successfully loaded from '{db_filename}' database, table '{table_name}'.")
    return df


# get all sales names
def get_sales() -> list[str]:
    '''
    docString
    parameter:
    return:
        傳出所有業務的名字
    '''
    try:
        conn = sqlite3.connect("sales_order1.db")
        with conn:
            # Create a cursor object to execute SQL commands
            cursor = conn.cursor()
            
            # SQL query to select unique sales from sales_orders1 table
            sql = '''
            SELECT DISTINCT "Sales Name"
            FROM sales_orders1
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