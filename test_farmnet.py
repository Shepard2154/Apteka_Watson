import farmnet
import requests


s = requests.Session()
web_api_session = farmnet.get_session_id(s, farmnet.CUSTOMER_ID, farmnet.PASSWORD)

print(farmnet.get_info_branch(s, web_api_session))
print(farmnet.get_products(s, web_api_session))
print(farmnet.get_product_remainder(s, web_api_session, 318919))

