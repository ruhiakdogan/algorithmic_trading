from regex import P
import websocket, json
from threading import Thread
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

cc = "xrpusdt"
socket = f"wss://stream.binance.com:9443/ws/{cc}@depth10"
socket2 = f"wss://ws.bitmex.com/realtime?subscribe=orderBook,orderBook10:{cc}"

binance_ask = 0
binance_bid = 0


def binance_on_message(ws, message):
    global binance_ask
    global binance_bid
    json_string = message
    a_json = json.loads(json_string)
    # print(a_json)
    binance_ask = a_json["asks"][0][0]
    binance_bid = a_json["bids"][0][0]
    # print("best bid " + a_json["bids"][0][0])  # best bid
    # print("best ask " + a_json["asks"][0][0])  # best ask
    sleep(1)


def binance_on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def bitmex_on_message(ws, message):
    global binance_ask
    global binance_bid
    json_string = message
    a_json = json.loads(json_string)
    # # print(a_json)
    # print(a_json["data"][0]["bids"][0][0])  # best bid
    # print(a_json["data"][0]["asks"][0][0])  # best ask
    bnc_bid = float(binance_bid)
    bnc_ask = float(binance_ask)
    bit_bid = float(a_json["data"][0]["bids"][0][0])
    bit_ask = float(a_json["data"][0]["asks"][0][0])
    print(bnc_bid)
    print(bnc_ask)
    print(bit_bid)
    print(bit_ask)
    # print("############")
    bid_farkı = (abs((bnc_bid - bit_bid) / bnc_bid)) * 100
    ask_farkı = (abs((bnc_ask - bit_ask) / bnc_ask)) * 100
    print("Bid Farkı: ", bid_farkı)
    print("Ask Farkı: ", ask_farkı)
    sleep(1)
    if bid_farkı > 0.6:
        print("YES")
        try:
            subcjet = "Arbitraj Bot"
            message = f"Arbitraj imkanı mevcut  Fark:%{bid_farkı}"
            content = "Subject: {0}\n\n{1}".format(subcjet, message)

            # Hesap Bilgileri
            myMailAdress = "mail@gmail.com"
            password = "password"

            # Kime Gönderilecek Bilgisi
            sendTo = "mail@gmail.com"

            mail = SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login(myMailAdress, password)
            mail.sendmail(myMailAdress, sendTo, content.encode("utf-8"))
            print("Mail Gönderme İşlemi Başarılı!")
        except Exception as e:
            print("Hata Oluştu!\n {0}".format(e))
    else:
        print("NO")

    sleep(1)


def bitmex_on_close(ws, close_status_code, close_msg):
    print("### closed ###")


if __name__ == "__main__":
    binance_ws = websocket.WebSocketApp(socket, on_message=binance_on_message, on_close=binance_on_close)
    bitmex_ws = websocket.WebSocketApp(socket2, on_message=bitmex_on_message, on_close=bitmex_on_close)
    wst2 = Thread(target=binance_ws.run_forever)
    wst = Thread(target=bitmex_ws.run_forever)
    wst.start()
    wst2.start()
