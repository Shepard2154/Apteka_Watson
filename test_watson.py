import watson


products = watson.get_all_products()
watson.beautify_products(products)

print(watson.check_product_existence(1022875)) # must return 43065
print(watson.check_product_existence(2222222222222222222)) # must return 0

watson.update_product(43065, 101, 2.0)
watson.create_product(123123213123123123123, 'сам себе доктор', 100, 'Россия', 1.0)