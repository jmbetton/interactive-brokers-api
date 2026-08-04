from ibapi.order import Order

def make_market_order(action, quantity):
    order = Order()
    order.action = action  # buy or sell
    order.orderType = 'MKT'
    order.totalQuantity = quantity
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order

def make_limit_order(action, quantity, limit_price):
    order = Order()
    order.action = action
    order.orderType = 'LMT'
    order.lmtPrice = limit_price
    order.totalQuantity = quantity
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order 
