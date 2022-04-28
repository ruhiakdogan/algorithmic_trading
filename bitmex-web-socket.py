import websocket, json

socket2 = f"wss://ws.bitmex.com/realtime?subscribe=orderBook,orderBook10:XRPUSD"

def bitmex_on_message(ws, message):
    json_string = message
    a_json = json.loads(json_string)
    #print(a_json)
    print(a_json["data"][0]["bids"][0][0]) # best bid
    print(a_json["data"][0]["asks"][0][0]) # best ask

def bitmex_on_close(ws, close_status_code, close_msg):
    print("### closed ###")

bitmex_ws = websocket.WebSocketApp(socket2, on_message=on_message, on_close=on_close)
bitmex_ws.run_forever()