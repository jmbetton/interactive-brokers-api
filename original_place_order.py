import time
from threading import Thread, Event
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order



class IBKRApp(EWrapper, EClient): # IBKRApp class inherits from both EWrapper and Eclient parent classes
    def __init__(self):
        EClient.__init__(self,self)
        self.next_order_id = None  # delivered by tws after connecting
        self.order_id_ready = Event()  # signal fires when ID arrives
    
    def nextValidId(self, orderId):
        self.next_order_id = orderId
        self.order_id_ready.set()  # flips signal to ready
    
    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=''):
        if errorCode not in (2104, 2106, 2158):
            print(f'Error {errorCode}: {errorString}')
    
    # add callbacks to IBKRApp 
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f'Order {orderId}: {status} | filled: {filled} @ avg {avgFillPrice}')
    
    def openOrder(self, orderId, contract, order, orderState):
        print(f'Open order {orderId}: {order.action} {order.totalQuantity} {contract.symbol} ({order.orderType})')


def connect_to_tws():
    app = IBKRApp()
    app.connect('127.0.0.1', 7497, clientId=124)

    api_thread = Thread(target=app.run, daemon=True)
    api_thread.start()

    ready = app.order_id_ready.wait(timeout=10)
    if not ready:
        raise ConnectionError('Never received nextValidId - Is TWS running with API enabled?')
        
    print(f'Connected. First order ID: {app.next_order_id}') 
        
    return app

def make_stock_contract(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    return contract
    
def make_market_order(action, quantity):
    order = Order()
    order.action = action  # buy or sell
    order.orderType = 'MKT'
    order.totalQuantity = quantity
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order

if __name__ == '__main__':
    app = connect_to_tws()

    contract = make_stock_contract('F')
    order = make_market_order('SELL', 1)

    order_id = app.next_order_id
    app.placeOrder(app.next_order_id, contract, order)
    print(f'Placed limit order {order_id}')

    time.sleep(5)
    app.disconnect()

    


