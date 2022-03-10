from datetime import datetime
import time

import farmnet
from loguru import logger
import requests
import watson


logger.add("main.log", format="{time}  {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')


while True:
    start_time = datetime.now().time()
    s = requests.Session()
    web_api_session = farmnet.get_session_id(s, farmnet.CUSTOMER_ID, farmnet.PASSWORD)

    logger.debug(f"downloading products...") 
    products = farmnet.get_products(s, web_api_session)
    logger.debug(f"downloaded {len(products)} products")            

    vendor_codes_of_unupdated_products = watson.get_vendor_code_of_all_products()

    count = 0
    for product in products:
        id = watson.check_product_existence(product.get('regId'))
        logger.debug(f"working with [{count+1}/{len(products)}] product from Farmnet") 
        logger.debug(product) 
        logger.debug(f"checking existense of {product.get('regId')} ({product.get('tovName')}) product in Watson...")
        count += 1
        if id:
            with open('vendor_codes.txt', 'w') as f:
                f.write(str(vendor_codes_of_unupdated_products))
            try:
                vendor_codes_of_unupdated_products.remove(str(product.get('regId')))
            except ValueError:
                logger.warning(f"product with this id has already updated") 

            updating = watson.update_product(id, int(product.get('price')), int(product.get('remainder')), {
                'Срок годности': product.get('Срок годности'),
                'Форма выпуска': product.get('Форма выпуска'),
                'Производитель': product.get('Производитель'),
                'Отпуск по рецепту': product.get('Отпуск по рецепту')
            }
            )
            logger.debug(f"updated [{count}/{len(products)}] product!")
            logger.debug(updating)  
        else:
            creating = watson.create_product(
                product.get('regId'), 
                product.get('tovName'), 
                int(product.get('price')), 
                product.get('fabr'), 
                float(product.get('remainder')),
                {
                    'Срок годности': product.get('Срок годности'),
                    'Форма выпуска': product.get('Форма выпуска'),
                    'Производитель': product.get('Производитель'),
                    'Отпуск по рецепту': product.get('Отпуск по рецепту')
                }
                )
            logger.debug(f"created [{count}/{len(products)}] product!")
            logger.info(creating)

    logger.debug(f"count of products with 0.0 remainder: {len(vendor_codes_of_unupdated_products)}")

    count = 0
    for vendor_code in vendor_codes_of_unupdated_products:
        id = watson.check_product_existence(vendor_code)
        nullifying = watson.nullify_product(id)
        count += 1
        logger.debug(f"nullified [{count}/{len(vendor_codes_of_unupdated_products)}] product!")
        logger.debug(nullifying)

    end_time = datetime.now().time()
    logger.debug(f"work time: {start_time} - {end_time}")
    logger.debug('--------------------------------------')

    time.sleep(3600*1.5)


    # Developer: burnaev1programmer
    # For questions and communications, write to https://vk.com/burnaev1programmer