import requests
# from src.core.config import settings

BOT_TOKEN = "1752591343:AAHvNFb73A4amAZ5dOd2xPgalsPOYjAxFW4"
# 135759089  kent0505
# 1093286245 OT4B3

try:
    response = requests.get("https://tonapi.io/v2/rates?tokens=ton&currencies=usd")
    if response.status_code == 200:
        data = response.json()
        ton_price = data["rates"]["TON"]["prices"]["USD"]
        diff_24h  = data["rates"]["TON"]["diff_24h"]["USD"]
        diff_7d   = data["rates"]["TON"]["diff_7d"]["USD"]
        diff_30d  = data["rates"]["TON"]["diff_30d"]["USD"]

        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
            data= {
                "chat_id": 1093286245,
                "text":    f"Toncoin\n\n${ton_price}\n24h {diff_24h}\n7d {diff_7d}\n30d {diff_30d}"
            }
        )
        if response.status_code == 200:
            print(response.status_code)
        else:
            print(response.status_code)
            print(response.text)
except Exception as e:
    print(e)