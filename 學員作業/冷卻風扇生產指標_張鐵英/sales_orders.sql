CREATE TABLE sales_orders(
	id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1),
	sales_id TEXT,
	sales_name TEXT,
	customer_id varchar(50),
	order_id TEXT,
	yield_rate REAL,
	thru_put REAL,
	order_date TEXT,
	deliver_date TEXT,
	factory TEXT,
	UNIQUE(customer_id)
)

