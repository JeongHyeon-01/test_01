import os, django, csv, sys


os.chdir('.')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sitwith.settings")

django.setup()
from products.models import *

CATEGORY_PATH = 'cores/csv/01_category.csv'

def insert_category():
    with open(CATEGORY_PATH, encoding='utf-8') as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader, None)
        for row in data_reader:
            # if not Category.objects.filter(name=row[1]).exists():
            if row[0]:
              Category.objects.create(
                    name =row[1]
                )

        


PRODUCTS_PATH = 'cores/csv/02_product.csv'

def insert_product():
    with open(PRODUCTS_PATH, encoding='utf-8') as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                Product.objects.create(
                    name =row[1],
                    price =row[2],
                    category = Category.objects.get(name=row[3].replace(' ','_'))
                )


COLORS_PATH = 'cores/csv/03_color.csv'

def insert_color():
    with open(COLORS_PATH, encoding='utf-8') as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                Color.objects.create(
                    name = row[1]
                )




IMAGE_PATH = 'cores/csv/05_image.csv'

def insert_images():
    with open(IMAGE_PATH, encoding='utf-8') as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader, None)
        for row in data_reader:
            color_id = Color.objects.get(name=row[3]).id
            product_id =Product.objects.get(name=row[4]).id
            product_color = ProductColor.objects.filter(color_id = color_id, product_id = product_id)
            for product in product_color:
                if row[0]:
                    Image.objects.create(
                        image_url =row[1],
                        sequence = row[2],
                        product_color = product
                    )



PRODUCTCOLOR_PATH = 'cores/csv/04_productcolor.csv'

def insert_productcolor():
    with open(PRODUCTCOLOR_PATH, encoding='utf-8') as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader, None)
        for row in data_reader:
            if row[0]:
                ProductColor.objects.create(
                    color = Color.objects.get(name=row[1]),
                    product=Product.objects.get(name=row[2]),
                    inventory = row[3]
                    
                )

# insert_category()
# insert_product()
# insert_color()
# insert_productcolor()
# insert_images()