import random
from datetime import datetime, timedelta
import pandas as pd
import sqlite3

def generate_sales_data(csv_filename='sales_orders.csv', db_filename='sales_orders.db', table_name='sales_orders'):
    # Step 1: Generate Orders and Sales Data

    import random

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

    # Randomly assign each sales representative between 2 to 6 customers
    assigned_customers = {}
    available_customers = customer_ids[:]  # Copy of customer IDs to avoid duplicates

    for sales_id in sales_ids:
        # Determine how many customers this sales rep will handle
        num_customers = random.randint(2, 6)
        # Assign customers, ensuring no duplicates
        customers = random.sample(available_customers, k=num_customers)
        for customer in customers:
            available_customers.remove(customer)
        assigned_customers[sales_id] = customers

    # Print the assigned customers for each sales representative
    for sales_id, customers in assigned_customers.items():
        print(f"{sales_id} ({sales_names[sales_ids.index(sales_id)]}): {customers}")

    # customer_ids = [f'Customer {i}' for i in range(1, 21)]
    order_ids = [f'2024-{str(i).zfill(2)}' for i in range(1, 51)]

    # Function to get the start date of a specific week in a given year
    def get_week_start(year, week):
        return datetime.strptime(f'{year}-W{str(week).zfill(2)}-1', "%Y-W%W-%w")

    # Initialize orders list
    orders = []

    # Generate random order dates, delivery dates, and factories
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

    # Step 2: Generate Sales Orders Data
    data = []

    # Assign each sales rep to approximately 5 customers
    for sales_id, sales_name in zip(sales_ids, sales_names):
        assigned_customers = random.sample(customer_ids, k=5)
        for customer in assigned_customers:
            # Each customer will have 3 to 4 orders
            num_orders = random.randint(3, 4)
            for _ in range(num_orders):
                order_id = random.choice(order_ids)
                yield_rate = round(random.uniform(96.1, 99.8), 2)
                thru_put = round(random.uniform(950, 1200), 2)

                # Find the matching order details from the orders list
                order_details = next((order for order in orders if order['Order ID'] == order_id), None)

                if order_details:
                    # Append the combined data to the data list
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

    # Step 3: Convert the Data to a DataFrame
    columns = ['sales_id', 'sales_name', 'customer_id', 'order_id', 'yield_rate',
               'thru_put', 'order_date', 'deliver_date', 'factory']
    df = pd.DataFrame(data, columns=columns)

    # Save the DataFrame to a CSV file
    df.to_csv(csv_filename, index=False)
    # print(f"CSV file '{csv_filename}' has been created successfully.")

    # Step 4: Import CSV into SQLite Database
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create a new table in the SQLite database
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Define the table schema with the additional fields
    create_table_query = f'''
    CREATE TABLE {table_name} (
        "sales_id" TEXT,
        "sales_name" TEXT,
        "customer_id" TEXT,
        "order_id" TEXT,
        "yield_rate" REAL,
        "thru_put" REAL,
        "order_date" TEXT,
        "deliver_date" TEXT,
        "factory" TEXT
    )
    '''
    cursor.execute(create_table_query)

    # Insert the data from the DataFrame into the SQLite database
    df.to_sql(table_name, conn, if_exists='append', index=False)

    # Commit and close the database connection
    conn.commit()
    conn.close()

    # print(f"Data from '{csv_filename}' has been successfully imported into '{db_filename}' database, table '{table_name}'.")
    return df
