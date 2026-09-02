import sys, time
sys.path.append('..') # searchs parent directory for packages

from ibkr.connection import connect_to_tws
from ibkr.contracts import make_stock_contract
from ibkr.orders import make_limit_order

if __name__ == '__main__':
    app = connect_to_tws()

    contract = make_stock_contract('F')
    order = make_limit_order('BUY', 1, 5.00)   # far below market rests unfilled

    order_id = app.next_order_id
    app.placeOrder(order_id, contract, order)
    print(f'Placed limit order {order_id}')

    time.sleep(5)

    app.cancelOrder(order_id, '')
    print(f'Cancel sent for order {order_id}')

    time.sleep(3)
    app.disconnect()