import math

from dotenv import load_dotenv
import os

from woocommerce import API


load_dotenv()

wcapi = API(
    url=os.getenv('DOMAIN'),
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    version='wc/v3',
    timeout=120
)


def get_vendor_code_of_all_products():
    products = get_all_products()
    vendor_codes = [str(product.get('sku')) for product in products]
    return vendor_codes


def get_all_products() -> list:
    """GET for getting of all products from WordPress-application"""
    page = 1
    all_products = []
    while True:
        products = wcapi.get('products', params={'per_page': 100, 'page': page}).json()
        if len(products) != 0:
            page += 1
            all_products += products
        else:
            return all_products
        

def beautify_products(products: list) -> None:
    """pretty printing of products"""
    for i in range(len(products)):
        print(f"[{i+1}/{len(products)}] id: {products[i].get('id')}, name: {products[i].get('name')}, price: {products[i].get('price')}")


def check_product_existence(sku: int) -> int:
    """GET for checking existense of product by vendor code (scu) for decision about creating or upgrading it"""
    product = wcapi.get(f"products/?sku={sku}").json()
    if len(product) == 0:
        return 0
    else:
        return product[0].get('id')


def update_product(id, price, count, attributes):
    "POST for product updating by ID in WordPress-application (not vendor code)"
    attributes = [
        {
            'id': 5,
            'name': 'Срок годности',
            'position': 1,
            'visible': True,
            'variation': False,
            'options': [attributes.get('Срок годности')] 
        },
        {
            'id': 7,
            'name': 'Форма выпуска',
            'position': 2,
            'visible': True,
            'variation': False,
            'options': [attributes.get('Форма выпуска')] 
        },
        {
            'id': 4,
            'name': 'Производитель',
            'position': 4,
            'visible': True,
            'variation': False,
            'options': [attributes.get('Производитель')]  
        },
        {
            'id': 6,
            'name': 'Отпуск по рецепту',
            'position': 5,
            'visible': True,
            'variation': False,
            'options': [str(attributes.get('Отпуск по рецепту'))]
        } 
    ]

    data = {
        "regular_price": f"{price}",
        "stock_quantity": f"{count}",
        'attributes': attributes,
        'manage_stock': True
    }
    return wcapi.put(f"products/{id}", data).json()


def nullify_product(id):
    data = {
        "stock_quantity": f"{0.0}",
        'manage_stock': True
    }
    return wcapi.put(f"products/{id}", data).json()


def create_product(sku: int, name: str, price: int, fabr: str, remainder: float, attributes: dict) -> dict:
    """POST for product creating"""
    attributes = [
        {
            'id': 5,
            'name': 'Срок годности',
            'position': 1,
            'visible': True,
            'variation': False,
            'options': [attributes.get('Срок годности')] 
        },
        {
            'id': 7,
            'name': 'Форма выпуска',
            'position': 2,
            'visible': True,
            'variation': False,
            'options': [attributes.get('Форма выпуска')] 
        },
        {
            'id': 4,
            'name': 'Производитель',
            'position': 4,
            'visible': True,
            'variation': False,
            'options': [attributes.get('Производитель')]  
        },
        {
            'id': 6,
            'name': 'Отпуск по рецепту',
            'position': 5,
            'visible': True,
            'variation': False,
            'options': [str(attributes.get('Отпуск по рецепту'))]
        } 
    ]

    data = {
        'sku': f"{sku}",
        'name': f"{name}",
        'regular_price': f"{price}",
        'short_description': f"{fabr}",
        'stock_quantity': f"{math.floor(remainder)}",
        'attributes': attributes,
        'manage_stock': True

    }
    return wcapi.post("products", data).json()