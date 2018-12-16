

from ordertree import OrderTree

class Orderbook(object):
    def __init__(self):
        self.bid = OrderTree()
        self.ask = OrderTree()
        self.time = 0

    def update_time(self):
        self.time += 1

    def process_order_list(self,side,order_list,quantity_still_to_trade,quote,output):
        trades = []
        quantity_to_trade = quantity_still_to_trade
        while len(order_list) and quantity_to_trade > 0 :
            head_order = order_list.get_head_order()
            traded_price = head_order.price
            if quantity_to_trade < head_order.quantity :
                traded_quantity = quantity_to_trade
                new_book_quantity = head_order.quantity - quantity_to_trade
                '''
                section for output
                '''
                print('{},{},{}'.format(output['trade_event'],traded_quantity,traded_price))
                print('{},{}'.format(output['fully_filled'], quote['order_id']))
                print('{},{},{},{}'.format(output['partial_filled'], head_order.order_id, head_order.side, new_book_quantity))
                head_order.update_quantity(new_book_quantity, head_order.timestamp)
                quantity_to_trade = 0
            elif quantity_to_trade == head_order.quantity:
                traded_quantity = quantity_to_trade
                print('{},{},{}'.format(output['trade_event'], traded_quantity, traded_price))
                print('{},{}'.format(output['fully_filled'], quote['order_id']))
                print('{},{}'.format(output['fully_filled'], head_order.order_id))
                if side == '0':
                    self.bid.remove_order_by_order_id(head_order.order_id)
                else:
                    self.ask.remove_order_by_order_id(head_order.order_id)
                quantity_to_trade = 0
            else:
                traded_quantity = head_order.quantity
                quantity_to_trade -= traded_quantity
                print('{},{},{}'.format(output['trade_event'], traded_quantity, traded_price))
                print('{},{},{},{}'.format(output['partial_filled'], quote['order_id'], quote['side'], quantity_to_trade))
                print('{},{}'.format(output['fully_filled'] , head_order.order_id))

                if side == '0':
                    self.bid.remove_order_by_order_id(head_order.order_id)
                else:
                    self.ask.remove_order_by_order_id(head_order.order_id)

        return quantity_to_trade

    def process_order(self, quote, output):
        order_in_book = None
        self.update_time()
        quote['timestamp'] = self.time
        if quote['quantity'] < 0 :
            print("BADMESSAGE : Quantity is less than 0")
            return
        quantity_to_trade = quote['quantity']
        side = quote['side']
        price = quote['price']

        if side == '0':
            while self.ask and price > self.ask.min_price() and quantity_to_trade > 0:
                best_price_ask = self.ask.min_price_list()
                quantity_to_trade = self.process_order_list('ask',best_price_ask,quantity_to_trade,quote,output)

            if quantity_to_trade > 0 :
                quote['quantity'] = quantity_to_trade
                self.bid.insert_order(quote)
                print("Order added in book")

        else:
            while self.bid and price < self.bid.max_price() and quantity_to_trade > 0 :
                best_price_bid =  self.bid.min_price_list()
                quantity_to_trade = self.process_order_list('bid',best_price_bid,quantity_to_trade,quote,output)

            if quantity_to_trade > 0 :
                quote['quantity'] = quantity_to_trade
                self.ask.insert_order(quote)
                print("Order added in book")

    def cancel_order(self ,order_id):
        self.update_time()
        if self.bid.order_exist(order_id):
            self.bid.remove_order_by_order_id(order_id)
            print("Order removed from order book")
        elif self.ask.order_exist(order_id):
            self.ask.remove_order_by_order_id(order_id)
            print("Order removed from order book")
        else:
            print ("Given Order does not exist")





