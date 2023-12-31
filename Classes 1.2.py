# TRY 1

class Product:
    def __init__(self, name, product_code, calories, expiry_days, quantity=1):
        self.name = name
        self.product_code = product_code
        self.calories = calories
        self.expiry_days = expiry_days
        self.quantity = quantity


class Dairy(Product):
    pass

class Fruit(Product):
    pass

class Vegetable(Product):
    pass

class Meat(Product):
    pass

class ApartmentFridge:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.owner in self.products:
            if len(self.products[product.owner]) < 1:
                self.products[product.owner].append(product)
                print(f"{product.name} added to the {product.owner}'s fridge.")
            else:
                print(f"The {product.owner}'s fridge is full!")
        else:
            self.products[product.owner] = [product]
            print(f"{product.name} added to a new {product.owner}'s fridge.")

    def display_fridge_contents(self):
        for owner, products in self.products.items():
            print(f"Owner: {owner}")
            for product in products:
                print(f" - {product.name} ({product.quantity} pieces)")


apartment_fridge = ApartmentFridge()

#Aufzählung der Produkte , bei "03" beliebigen code einfügen für streamlit, kalorien, Expiry Days, Quantität

sausage_A = Meat("Sausage", "03", "1200", 5, quantity=1)
sausage_B = Meat("Sausage", "03", "1200", 5, quantity=1)
milk_A = Dairy("Milk", "02", "0400", 7, quantity=1)
milk_B = Dairy("Milk", "02", "0400", 7, quantity=1)
apple_A = Fruit("Apple", "04", "0300", 10, quantity=1)
apple_B = Fruit("Apple", "04", "0300", 10, quantity=1)
tomatoes_A = Vegetable("Tomatoes", "05", "0200", 4, quantity=1)
tomatoes_B = Vegetable("Tomatoes", "05", "0200", 4, quantity=1)


apartment_fridge.add_product(sausage_A)
apartment_fridge.add_product(sausage_B)
apartment_fridge.add_product(milk_A)
apartment_fridge.add_product(milk_B)
apartment_fridge.add_product(apple_A)
apartment_fridge.add_product(apple_B)
apartment_fridge.add_product(tomato_A)
apartment_fridge.add_product(tomato_B)


apartment_fridge.display_fridge_contents()

-----------------------------------------------------------------------

#TRY 2




class Product:
    def __init__(self, name, product_code, calories, expiry_days, owner, quantity=1):
        self.name = name
        self.product_code = product_code
        self.calories = calories
        self.expiry_days = expiry_days
        self.owner = owner
        self.quantity = quantity


class Dairy(Product):
    pass

class Fruit(Product):
    pass

class Vegetable(Product):
    pass

class Meat(Product):
    pass

class ApartmentFridge:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.owner in self.products:
            if not self.products[product.owner]:  
                self.products[product.owner].append(product)
                print(f"{product.name} added to the {product.owner}'s fridge.")
            else:
                print(f"The {product.owner}'s fridge is full!")
        else:
            self.products[product.owner] = [product]
            print(f"{product.name} added to a new {product.owner}'s fridge.")

    def display_fridge_contents(self):
        for owner, products in self.products.items():
            print(f"Owner: {owner}")
            for product in products:
                print(f" - {product.name} ({product.quantity} pieces)")

apartment_fridge = ApartmentFridge()

#Aufzählung der Produkte , bei "03" beliebigen code einfügen für streamlit, kalorien, Expiry Days, owner,  Quantität

sausage_A = Meat("Sausage", "03", "1200", 3, "Eric" ,  quantity=1)
sausage_B = Meat("Sausage", "03", "1200", 3, "Simona", quantity=1)
milk_A = Dairy("Milk", "02", "0400", 7, "Lorenzo", quantity=1)
milk_B = Dairy("Milk", "02", "0400", 7, "Raffaello", quantity=1)
apple_A = Fruit("Apple", "04", "0300", 10, "Anina", quantity=1)
apple_B = Fruit("Apple", "04", "0300", 10, "Lorenzo", quantity=1)
tomatoes_A = Vegetable("Tomatoes", "05", "0200", 5, "Max",  quantity=1)
tomatoes_B = Vegetable("Tomatoes", "05", "0200", 5, "Moritz", quantity=1)


apartment_fridge.add_product(sausage_A)
apartment_fridge.add_product(sausage_B)
apartment_fridge.add_product(milk_A)
apartment_fridge.add_product(milk_B)
apartment_fridge.add_product(apple_A)
apartment_fridge.add_product(apple_B)
apartment_fridge.add_product(tomato_A)
apartment_fridge.add_product(tomato_B)


apartment_fridge.display_fridge_contents()
