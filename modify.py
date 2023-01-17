import dbconfig
db = dbconfig.getDB()
collection = db.products

def modify_name(id):
    """Modify product name"""
    choice1 = input('Do you want to modify the product name? (y/N): ')
    if choice1=="y":
        new_name = input('Change name to something else > ')
        entries = collection.find()
        for entry in entries:
            if id == entry['_id']:
                try:
                    updated_prod = {
                        'name':new_name,'price':entry['price'],'category':entry['category'],'color':entry['color']
                    }
                    collection.find_one_and_replace({'_id': id}, updated_prod)                
                except NameError:
                    print(NameError)
                   

def modify_category(id):
    """Modify product category"""
    choice1 = input('Do you want to modify the product category? (y/N): ')
    if choice1=="y":
        new_category = input('Change category to something else > ')
        entries = collection.find()
        for entry in entries:
            if id == entry['_id']:
                try:
                    updated_prod = {
                        'name':entry['name'],'price':entry['price'],'category':new_category,'color':entry['color']
                    }
                    collection.find_one_and_replace({'_id': id}, updated_prod)                
                except NameError:
                    print(NameError)
       

def delete_product(id):
    """Delete product"""
    choice1 = input('Do you want to delete the present product? (y/N): ')
    if choice1=="y":
        entries = collection.find()
        for entry in entries:
            if id == entry['_id']:
                try:
                    collection.find_one_and_delete({'_id':id})
                    break
                except NameError:
                    print(NameError)
       
        
        