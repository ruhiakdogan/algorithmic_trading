import websocket, json

cc = "btcusdt"
socket = f"wss://stream.binance.com:9443/ws/{cc}@depth10"

def on_message(ws, message):
    json_string = message
    a_json = json.loads(json_string)
    print(a_json)
    print(a_json["bids"][0][0]) # best bid
    print(a_json["asks"][0][0]) # best ask

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
ws.run_forever()
