from threading import Event
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

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
