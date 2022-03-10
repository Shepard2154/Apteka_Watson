import farmnet
import requests
from datetime import datetime


s = requests.Session()
web_api_session = farmnet.get_session_id(s, farmnet.CUSTOMER_ID, farmnet.PASSWORD)

# print(farmnet.get_info_branch(s, web_api_session))
# print(farmnet.get_products(s, web_api_session))

eutiroks = [808658, 230998, 81138, 57713, 57712, 56357, 23447, "57713-1", "230998-1", 56355, "57712-1", 1203727]
for item in eutiroks:
    print(farmnet.get_product_remainder(s, web_api_session, item))




# print(farmnet.get_form_product(s, web_api_session, product.get('regId')))


# products = farmnet.download_products(s, web_api_session, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# print(len(products.get("items")))

# ids = []
# for product in products.get("items"):
#     print(farmnet.get_filter_fields(s, web_api_session, product, product.get('regId')))
#     ids.append(product.get('regId'))

# print(len(set(ids)))