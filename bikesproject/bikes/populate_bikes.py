import os
import sys
import django
import csv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikesproject.settings')

django.setup()

from bikes.models import Bike

csv_file_path = os.path.join(os.path.dirname(__file__), 'bikes_data.csv')

def populate_bikes():
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                CATEGORY_MAPPING = {
                    'Scooty': 'scooty',
                    'Gear Bike': 'gear-bike',
                    'EV': 'ev'
                }
                kilometers_driven = float(row['Kilometers Driven'])
                price_per_month = float(row['Price per month'])
                price_per_day = float(row['Price per Day'])
                description = row.get('Description', '')  
                purchase_date = row.get('Purchase Date', None)

                status = False if row['Status'] == 'False' else True

                category = CATEGORY_MAPPING.get(row['Category'], '').lower()
                if not category:
                    print(f"No valid category mapping found for {row['Name']} with category {row['Category']}")
                    continue

                bike = Bike(
                    category=category,
                    name=row['Name'],
                    price_per_month=price_per_month,
                    price_per_day=price_per_day,
                    registration_number=row['Registration Number'],
                    imagefile=row['imagefile'],
                    purchase_date=purchase_date,
                    model_name=row['Model Name'],
                    status=status,
                    brand_name=row['Brand Name'],
                    city=row['City'],
                    description=description,
                    kilometers_driven=kilometers_driven,
                    location=row['Location']
                )
                bike.save()
            except ValueError as e:
                print(f"Skipping row due to data error: {e}, row data: {row}")

    print("Bike data has been populated.")

if __name__ == '__main__':
    populate_bikes()
