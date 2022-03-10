import watson


# products = watson.get_all_products()
# watson.beautify_products(products)

print(watson.check_product_existence(1022875)) # must return 43065
print(watson.check_product_existence(2222222222222222222)) # must return 0

# watson.update_product(43065, 101, 2.0)

attributes1 = {
    'Срок годности': '2023-04-30',
    'Форма выпуска': 'Левотироксин натрия',
    'Производитель': 'Berlin-Chemie AG/Германия',
    'Отпуск по рецепту': 'False'
}

attributes2 = {
    'Срок годности': '2024-04-30',
    'Форма выпуска': 'Левотироксин натрияяяяяя',
    'Производитель': 'Berlin-Chemie AG/Германияяяяяяяя',
    'Отпуск по рецепту': 'True'
}

# creating = watson.create_product(123123213123123123123, 'сам себе доктор', 100, 'Россия', 3.0, attributes1)
# print(creating)
updating = watson.update_product(46303, 105, 5, attributes1)
print(updating)
