import sys, time
sys.path.append('..') 

from ibkr.connection import connect_to_tws
from ibkr.contracts import make_stock_contract
from ibkr.orders import make_market_order

if __name__ == '__main__':
    app = connect_to_tws()

    contract = make_stock_contract('F')
    order = make_market_order('BUY', 1)

    order_id = app.next_order_id
    app.placeOrder(order_id, contract, order)
    print(f'Placed market order {order_id}')

    time.sleep(5)
    app.disconnect()

    