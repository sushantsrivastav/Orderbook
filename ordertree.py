from avltree import AVLTree
from orderlist import OrderList
from order import Order


class OrderTree(object):
    def __init__(self):
        self.price_tree = AVLTree()
        self.price_map = {}
        self.order_map = {}
        self.volume = 0
        self.num_orders = 0
        self.depth = 0

    def __len__(self):
        return len(self.order_map)

    def get_price_list(self,price):
        return self.price_map[price]

    def get_order(self,order_id):
        return self.order_map[order_id]

    def create_price(self,price):
        self.depth += 1
        new_list = OrderList()
        self.price_tree.insert(price,new_list)
        self.price_map[price] = new_list

    def remove_price(self,price):
        self.depth -= 1
        self.price_tree.remove(price)
        del self.price_map[price]

    def price_exists(self,price):
        return price in self.price_map

    def order_exist(self,order):
        return order in self.order_map

    def insert_order(self, quote):
        if self.order_exist(quote['order_id']):
            self.remove_order_by_order_id(quote['order_id'])
        self.num_orders += 1
        if quote['price'] not in self.price_map:
            self.create_price(quote['price'])
        order = Order(quote, self.price_map[quote['price']])
        self.price_map[order.price].append_order(order)
        self.order_map[order.order_id] = order
        self.volume += order.quantity

    def remove_order_by_order_id(self,order_id):
        self.num_orders -= 1
        order = self.order_map[order_id]
        self.volume -= order.quantity
        order.order_list.remove_order(order)
        if len(order.order_list) == 0 :
            self.remove_price(order.price)
        del self.order_map[order_id]

    def max_price(self):
        if self.depth > 0 :
            return self.price_tree.max_key()
        else :
            return None

    def min_price(self):
        if self.depth > 0 :
            return self.price_tree.min_key()
        else :
            return None

    def max_price_list(self):
        if self.depth > 0 :
            return self.get_price_list(self.max_price())
        else:
            return None

    def min_price_list(self):
        if self.depth > 0 :
            return self.get_price_list(self.min_price())
        else :
            return None





