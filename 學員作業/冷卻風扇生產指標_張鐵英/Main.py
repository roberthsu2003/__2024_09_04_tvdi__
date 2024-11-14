from ttkthemes import ThemedTk
from datasource import generate_orders, generate_sales_orders, save_to_csv, save_to_sqlite, load_from_sqlite


class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    print("Hello Tkinter and Python")
    pass






def main():
   # Step 1: Generate orders
    orders = generate_orders()

    # Step 2: Generate sales orders data
    sales_data = generate_sales_orders(orders)

    # Step 3: Save sales data to CSV
    df = save_to_csv(sales_data)

    # Step 4: Save sales data to SQLite database
    save_to_sqlite(df)

    # Step 5: Load data back from SQLite database for verification
    loaded_df = load_from_sqlite()
    print("\nLoaded Data from SQLite:")
    print(loaded_df.head())
    
    window = Window(theme="arc")
    window.mainloop()



if __name__ == '__main__':
    main()