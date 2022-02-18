import pandas as pd
import websocket, json

cc = "btcusdt"
socket = f"wss://stream.binance.com:9443/ws/{cc}@depth10"

def on_message(ws, message):
    json_string = message
    a_json = json.loads(json_string)
    # print(a_json)

    df = pd.DataFrame.from_dict(a_json)
    # print(df)
    del df["lastUpdateId"]
    df["bid_price"] = pd.to_numeric(df["bids"].str[0])
    df["bid_qnt"] = pd.to_numeric(df["bids"].str[1])
    df["ask_price"] = pd.to_numeric(df["asks"].str[0])
    df["ask_qnt"] = pd.to_numeric(df["asks"].str[1])
    del df["bids"]
    del df["asks"]
    print(df)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
ws.run_forever()