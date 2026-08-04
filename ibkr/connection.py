from threading import Thread
from ibkr.app import IBKRApp

def connect_to_tws(client_id=124):
    app = IBKRApp()
    app.connect('127.0.0.1', 7497, clientId=client_id)

    api_thread = Thread(target=app.run, daemon=True)
    api_thread.start()

    ready = app.order_id_ready.wait(timeout=10)
    if not ready:
        raise ConnectionError('Never received nextValidId - Is TWS running with API enabled?')
        
    print(f'Connected. First order ID: {app.next_order_id}') 
        
    return app
