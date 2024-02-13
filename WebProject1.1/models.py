class user:
    def __init__(self, name, email, pwd):
        self.username = name
        self.email = email
        self.password = pwd


class contact:
    def __init__(self, email, address, phone, city):
        self.email = email
        self.address = address
        self.phone = phone
        self.city = city

class orders:
    def __init__(self,  user_email,  total_amount):
        self.user_email = user_email
        self.total_amount = total_amount

class orders_items:
    def __init__(self, item_name, price, quantity):
        self.item_name = item_name
        self.price = price
        self.quantity = quantity

