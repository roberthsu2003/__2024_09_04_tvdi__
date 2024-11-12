import pandas as pd
import numpy as np
import random

# Initialize sales and customers
sales = ['Sales A', 'Sales B', 'Sales C', 'Sales D', 'Sales E']
customers = [f'Customer {i}' for i in range(1, 21)]

# Shuffle customers randomly
random.shuffle(customers)

# Split customers into 5 groups (each group will have around 4-5 customers)
customer_groups = [customers[i::5] for i in range(5)]

# Create a dictionary to store sales and their assigned customers
sales_dict = {sales[i]: customer_groups[i] for i in range(5)}

# Convert to pandas DataFrame
max_customers_per_sale = max(len(group) for group in customer_groups)
sales_df = pd.DataFrame.from_dict(sales_dict, orient='index')

# Fill empty cells with NaN for a clear layout
sales_df = sales_df.apply(lambda x: pd.Series(x.dropna().tolist() + [None]*(max_customers_per_sale-len(x))), axis=1)

# Rename columns for clarity
sales_df.columns = [f'Customer {i+1}' for i in range(sales_df.shape[1])]

# Display the DataFrame
print("Sales vs Customers Assignment Table:")
print(sales_df)
