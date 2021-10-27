from datetime import datetime
from dotenv import load_dotenv
import json 
import os


load_dotenv()

PROVIDER_DOMAIN = os.getenv('PROVIDER_DOMAIN')
CUSTOMER_ID = os.getenv('CUSTOMER_ID')
PASSWORD =  os.getenv('PASSWORD')


def get_session_id(session, customer_id: int, password: str) -> str:
    """GET to get a session token"""
    url = PROVIDER_DOMAIN + f"Login?customerId={customer_id}&password={password}"
    request = session.get(url)
    data = json.loads(request.text)
    return data.get('sessionId')


def get_info_branch(session, web_api_session: str) -> dict:
    """GET to get info about provider"""
    url = PROVIDER_DOMAIN + 'BranchList'
    request = session.get(url=url, headers={'WebApiSession': web_api_session})
    data = json.loads(request.text)
    return data
    

def get_product_remainder(session, web_api_session: str, id: int) -> dict:
    """GET to get info about remainder product by id"""
    url = PROVIDER_DOMAIN + f'OstByGoods?regId={id}'
    request = session.get(url=url, headers={'WebApiSession': web_api_session})
    data = json.loads(request.text)
    return data


def download_products(session, web_api_session: str, datetime: datetime) -> dict:
    """GET to download all products of provider with id=13889 and current datetime"""
    url = PROVIDER_DOMAIN + f'OstByDate?branchId=13889&date={datetime}'
    request = session.get(url=url, headers={'WebApiSession': web_api_session})
    data = json.loads(request.text)
    return data


def get_products(s, web_api_session: str) -> list:
    """parser of important fields of downloaded products"""
    products = []
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_products = download_products(s, web_api_session, date)
    for product in all_products.get("items"):
        products.append(
            {
                'regId': product.get('regId'),
                'tovName': product.get('tovName'),
                'price': product.get('priceRoznWNDS'),
                'recipe': product.get('recipe'),
                'fabr': product.get('fabr'),
                'remainder': product.get('uQntOst')                
            }
        )
    return products
