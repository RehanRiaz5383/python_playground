import pandas as pd
import random
from datetime import datetime, timedelta

# Data ki tadaad set karein
num_records = 5000

# Products aur unki realistic price ranges (PKR main)
products = {
    'iPhone 15': {'category': 'Mobile', 'min_p': 250000, 'max_p': 350000},
    'Samsung S24': {'category': 'Mobile', 'min_p': 220000, 'max_p': 300000},
    'Google Pixel 8': {'category': 'Mobile', 'min_p': 180000, 'max_p': 250000},
    'MacBook Air M2': {'category': 'Laptop', 'min_p': 300000, 'max_p': 400000},
    'Dell XPS 13': {'category': 'Laptop', 'min_p': 280000, 'max_p': 380000},
    'Airpods Pro': {'category': 'Accessories', 'min_p': 45000, 'max_p': 65000},
    'Sony WH-1000XM5': {'category': 'Accessories', 'min_p': 80000, 'max_p': 105000},
    'Mechanical Keyboard': {'category': 'Accessories', 'min_p': 10000, 'max_p': 25000}
}
payment_methods = ['Cash', 'Credit Card', 'JazzCash', 'EasyPaisa']

data = []
start_date = datetime.now() - timedelta(days=365) # Pichle 1 saal ka data

# 1000 records generate karne ka loop
for i in range(1, num_records + 1):
    product_name = random.choice(list(products.keys()))
    prod_info = products[product_name]
    
    # Random date nikalna
    random_days = random.randint(0, 365)
    order_date = start_date + timedelta(days=random_days)
    
    record = {
        'Order_ID': f"ORD-{10000+i}",
        'Date': order_date.strftime('%Y-%m-%d'),
        'Product': product_name,
        'Category': prod_info['category'],
        'Price': random.randint(prod_info['min_p'], prod_info['max_p']),
        'Quantity': random.randint(1, 5),
        'Payment_Method': random.choice(payment_methods)
    }
    data.append(record)

# Dataframe banana aur CSV main save karna
df = pd.DataFrame(data)
df.to_csv('sales_data.csv', index=False)

print(f"✅ Mubarak ho! {num_records} records ki 'sales_data.csv' file aapke folder main ban gayi hai.")