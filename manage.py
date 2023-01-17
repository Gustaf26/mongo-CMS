"""Products db where you can add your products, modify them and delete 
each of them or a whole collection"""

"""I follow PyMongo syntax for queries, available at https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html"""

from collections import OrderedDict
import os
import modify
import dbconfig
import pdb
from bson.objectid import ObjectId


db = dbconfig.getDB()
collection = db.products

class Product():
    
    """Model for creating products"""
    def __init__(self, price, name, category, color, in_store):
        self.price = price 
        self.name = name
        self.category= category
        self.color = color
        self.in_store=in_store
        
class Action():

    """Model for products actions"""
    def __init__(self):
        # An OrderedDict is a dictionary that remembers the order that keys were first inserted. 
        # OrderedDict preserves the order in which the keys are inserted. 
        self.main_menu = OrderedDict([
            ('a', add_product),
            ('m', modify_product),
            ('c', cleanup_products),
            ('s',show_categories),
            ('mc',modify_by_category),
            ('v', search_by_value)
        ])

        self.sub_menu = OrderedDict([
            ('m', modify.modify_name),
            ('d', modify.modify_category),
            ('e', modify.delete_product)
        ])

def clear():
    """Clear the display"""
    os.system('cls' if os.name == 'nt' else 'clear')


# Function to view products
def view_products():
    """"View products list"""

    entries = collection.find()
    for entry in entries:
        print(entry['_id'],entry['name'],entry['category'],entry['color'],entry['price'])

    print('\nMY PRODUCTS LIST')
    print('=' * 40)

    return entries  

# Function to add a new product
def add_product():
    """Add a new product"""
    prod_name = input('\nProduct name: ')
    prod_category = input('Write category: ')
    prod_price = input('\nEnter price: ')
    prod_color = input('\nEnter color: ')
    prod_in_store = input('\nIn store (true / false): ')

    newProd = Product(prod_price, prod_name, prod_category, prod_color, prod_in_store)
    prodInfo = {'price':newProd.price, 'name':newProd.name, 'category':newProd.category,'color':newProd.color, 'in_store':newProd.in_store}
    result = collection.insert_one(prodInfo)
    pdb.set_trace()
    view_products()

# Function to modify an existing to do taken by id
def modify_product():
    """Modify selected product"""
    id = input('Enter id of task')
    print('\n\n')
    # What happens if id is not in db or if id is not a number? 
    # We need to make a try - except and loop through the db first and
    #  find / not find the id

    newAction = Action()
    # Loop through submenu to see what we wanna do with the to do
    for key, value in newAction.sub_menu.items():
        print('{}) {}'.format(key, newAction.sub_menu[key].__doc__))
    print('q) Back to Main')
    next_action = input('Action: ')

    # Action to be taken, each action imported from modify.py
    if next_action.lower().strip() in newAction.sub_menu:
        # Funktionerna i modify.py körs (en vald funktion)
        newAction.sub_menu[next_action](ObjectId(id))
        # Körs efter att den funktionen körts
        view_products()
    else:
        return

def show_categories():
    """Show the different product categories"""
    entries = collection.find()
    prod_categories=[]
    for entry in entries:
        if not entry['category'] in prod_categories:
            prod_categories.append(entry['category'])
    print(prod_categories)

def search_by_value():
    """Search products by a parameter && value"""
    par_name = input('Which products parameter do you want to see (category / name / color / price)?: ')
    par_value = input("Which value shall be found in product parameter?: ")
    entries = collection.find({f'{par_name}':par_value})
    prods_in_category=[]
    for entry in entries:
        prods_in_category.append(entry)
    else:
        print(prods_in_category)


def modify_by_category():
    """Modify a value for all products in a category"""
    cat_name = input('Which category products do you want to modify?: ')
    field = input('Which property do you want to update?: ')
    field_value = input('Which value do you want to set?: ')
    collection.update_many({"category":cat_name},{"$set": { field : field_value }})
    view_products()



def cleanup_products():
    """Cleanup: delete of all products"""
    if (input('Are you sure you want to delete the done tasks? [yN]').lower().strip() == 'y'):
        db.collection.drop()
        view_products()


def menu_loop():
    choice = None
    
    entries = view_products()
    while choice != 'q':
        if entries:
            print('\n' + '=' * 40 + '\n')

        #The items() method returns a view object. 
        # The view object contains the key-value pairs of the dictionary, 
        # as tuples in a list.
        newAction = Action()
        for key, value in newAction.main_menu.items():
            print(f'{key}) {value.__doc__}')
        print('q) Quit')

        choice = input('\nAction: ')
        if choice in newAction.main_menu:
            try:
                newAction.main_menu[choice]()
            except ZeroDivisionError:
                continue

menu_loop()
