from datetime import datetime
import time

import farmnet
from loguru import logger
import requests
import watson


logger.add("main.log", format="{time}  {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

start_time = datetime.now().time()

while True:
    s = requests.Session()
    web_api_session = farmnet.get_session_id(s, farmnet.CUSTOMER_ID, farmnet.PASSWORD)

    products = farmnet.get_products(s, web_api_session)
    logger.debug(f"downloaded {len(products)} products")            

    count = 0
    for product in products:
        id = watson.check_product_existence(product.get('regId'))
        logger.debug(f"working with [{count+1}/{len(products)}] product from Farmnet") 
        logger.debug(product) 
        logger.debug(f"checking existense of {product.get('regId')} ({product.get('tovName')}) product in Watson...")
        count += 1
        if id:
            updating = watson.update_product(id, int(product.get('price')), float(product.get('remainder')))
            logger.debug(f"updated [{count}/{len(products)}] product!")
            logger.debug(updating)  
        else:
            creating = watson.create_product(
                product.get('regId'), 
                product.get('tovName'), 
                int(product.get('price')), 
                product.get('fabr'), 
                product.get('remainder')
                )
            logger.debug(f"created [{count}/{len(products)}] product!")
            logger.info(creating)

    end_time = datetime.now().time()
    logger.debug(f"work time: {start_time} - {end_time}")
    logger.debug('--------------------------------------')

    time.sleep(3600*1.5)


    # Developer: burnaev1programmer
    # For questions and communications, write to https://vk.com/burnaev1programmer