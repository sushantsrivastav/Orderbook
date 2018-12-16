import orderbook
from decimal import *

order_book = orderbook.Orderbook()
output = {'trade_event': 2,
          'fully_filled': 3,
          'partial_filled':4}

while True:
    input_value = raw_input("Enter the new order in comma separated or Enter Quit\n")
    if input_value == 'Quit':
        break
    elif input_value == None :
        print("BADMESSAGE : No value provided")
        continue
    else:
        input_list = input_value.split(',')
        quote = {}
        quote['input_message_type'] = input_list[0]
        if quote['input_message_type'] == '0':
            if len(input_list) != 5:
                print("BADMESSAGE : Some values are missing or extra in last message")
                continue
            else:
                quote['order_id'] = int(input_list[1])
                quote['side'] = input_list[2]
                if quote['side'] != '0' and quote['side'] != '1':
                    print("BADMESSAGE : value for side is neither bid(0) nor ask(1)")
                    continue
                quote['quantity'] = Decimal(input_list[3])
                quote['price'] = Decimal(input_list[4])
                order_book.process_order(quote, output)
        elif quote['input_message_type'] == '1':
            if len(input_list) != 2:
                print("BADMESSAGE : Some values are missing or extra in last message")
                continue
            else:
                quote['order_id'] = int(input_list[1])
                order_book.cancel_order(quote['order_id'])
        else:
            print("BADMESSAGE : Please enter valid action, 0(AddOrder) or 1(CancelOrder)")
            continue









