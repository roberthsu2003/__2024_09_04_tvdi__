import random
from datetime import datetime, timedelta
import pandas as pd
import sqlite3

def generate_sales_data(csv_filename='sales_orders.csv', db_filename='sales_orders.db', table_name='sales_orders'):
    # Updated sales IDs and names
    sales_ids = ['Sales_A', 'Sales_B', 'Sales_C', 'Sales_D', 'Sales_E']
    sales_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']

    # Updated customer names from the cooling fan industry
    customer_ids = [
        'Foxconn', 'Delta_Electronics', 'Nidec', 'SanAce', 'Cooler_Master',
        'Be_Quiet', 'Noctua', 'Corsair', 'NZXT', 'Arctic',
        'Phanteks', 'Thermaltake', 'Fractal_Design', 'Lian_Li', 'DeepCool',
        'AeroCool', 'SilverStone', 'Cougar', 'Scythe', 'Antec'
    ]

    # Assign each sales representative a random number of customers (2 to 6)
    assigned_customers = {}
    available_customers = customer_ids[:]

    for sales_id in sales_ids:
        num_customers = random.randint(2, 6)
        customers = random.sample(available_customers, k=num_customers)
        assigned_customers[sales_id] = customers
        for customer in customers:
            available_customers.remove(customer)

    # Generate orders
    order_ids = [f'2024-{str(i).zfill(2)}' for i in range(1, 51)]

    def get_week_start(year, week):
        """Get the start date of a specific week in a given year."""
        return datetime.strptime(f'{year}-W{str(week).zfill(2)}-1', "%Y-W%W-%w")

    orders = []
    for order_id in order_ids:
        order_week = int(order_id.split('-')[1])
        order_week_start = get_week_start(2024, order_week)
        order_date = order_week_start - timedelta(weeks=random.choice([1, 2]), days=random.randint(0, 6))
        delivery_date = order_week_start + timedelta(weeks=random.choice([4, 5]), days=random.randint(0, 6))
        factory = random.choice(['China', 'Vietnam'])
        orders.append({
            'Order ID': order_id,
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Delivery Date': delivery_date.strftime('%Y-%m-%d'),
            'Factory': factory
        })

    # Generate sales orders
    data = []
    for sales_id, sales_name in zip(sales_ids, sales_names):
        customers = assigned_customers[sales_id]
        for customer_id in customers:
            num_orders = random.randint(3, 6)  # Each customer has 3–6 orders
            for _ in range(num_orders):
                order_details = random.choice(orders)
                data.append([
                    sales_id,
                    sales_name,
                    customer_id,
                    order_details['Order ID'],
                    round(random.uniform(96.1, 99.8), 2),  # Yield Rate
                    round(random.uniform(950, 1200), 2),  # Thru-put
                    order_details['Order Date'],
                    order_details['Delivery Date'],
                    order_details['Factory']
                ])

    # Convert to DataFrame
    columns = ['sales_id', 'sales_name', 'customer_id', 'order_id', 'yield_rate', 'thru_put', 'order_date', 'deliver_date', 'factory']
    df = pd.DataFrame(data, columns=columns)

    # Save DataFrame to CSV
    df.to_csv(csv_filename, index=False)
    print(f"CSV file '{csv_filename}' created successfully.")

    # Create SQLite database and table
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")  # Caution: Drop the table to avoid duplicates

    create_table_query = f'''
    CREATE TABLE {table_name} (
        sales_id TEXT,
        sales_name TEXT,
        customer_id TEXT,
        order_id TEXT,
        yield_rate REAL,
        thru_put REAL,
        order_date TEXT,
        deliver_date TEXT,
        factory TEXT
    )
    '''
    cursor.execute(create_table_query)

    # Insert DataFrame into SQLite
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    print(f"Data successfully imported into '{db_filename}', table '{table_name}'.")

    return df
