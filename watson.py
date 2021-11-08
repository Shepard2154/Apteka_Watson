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


def update_product(id: int, price: int, count: float, attributes: dict) -> dict:
    "POST for product updating by ID in WordPress-application (not vendor code)"
    attributes = [
        {
            'name': 'Срок годности',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [attributes.get('Срок годности')] 
        },
        {
            'name': 'Форма выпуска',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [attributes.get('Форма выпуска')] 
        },
        {
            'name': 'Производитель',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [attributes.get('Производитель')]  
        },
        {
            'name': 'Отпуск по рецепту',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [str(attributes.get('Отпуск по рецепту'))]
        } 
    ]


    data = {
        "regular_price": f"{price}",
        "stock_quantity": f"{count}",
        'attributes': attributes
    }
    return wcapi.put(f"products/{id}", data).json()


def create_product(sku: int, name: str, price: int, fabr: str, remainder: float, attributes: dict) -> dict:
    """POST for product creating"""
    attributes = [
        {
            'name': 'Срок годности',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [attributes.get('Срок годности')] 
        },
        {
            'name': 'Форма выпуска',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [attributes.get('Форма выпуска')] 
        },
        {
            'name': 'Производитель',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [attributes.get('Производитель')]  
        },
        {
            'name': 'Отпуск по рецепту',
            "position": 0,
            "visible": False,
            "variation": True,
            'options': [str(attributes.get('Отпуск по рецепту'))]
        } 
    ]

    data = {
        'sku': f"{sku}",
        'name': f"{name}",
        'regular_price': f"{price}",
        'short_description': f"{fabr}",
        'stock_quantity': f"{float(remainder)}",
        'attributes': attributes

    }
    return wcapi.post("products", data).json()