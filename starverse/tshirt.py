import requests
import json
import pandas as pd

address_star = {}

def get_user_token(address):
    url = f"https://scan.testnet.verichains.xyz/api?module=account&action=tokenbalance&address={address}&contractaddress=0x82a29828a3B5c16ed13Dc7840D0699746D2a741C"
    payload = ""
    headers = {}

    res = requests.request("GET", url, headers=headers, data=payload).json()

    return int(res["result"]) / 10**18

def get_token_holders(size=10):
    url = f"https://scan.testnet.verichains.xyz/api?module=token&action=getTokenHolders&contractaddress=0x82a29828a3B5c16ed13Dc7840D0699746D2a741C&offset={size}"

    payload = ""
    headers = {}

    res = requests.request("GET", url, headers=headers, data=payload).json()

    address_star = {}
    for h in res["result"]:
        address_star[h["address"]] = int(h["value"])/10**18

    return address_star

def get_tshirt(id):
    url = "https://api.yoverse.io/marketplace/rpc"

    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "vmp_listNFTBidding",
        "params": {
            "offset": 0,
            "limit": 10,
            "contractAddress": "0x5AF3a83b777cb1a862Efe672AFb645E32cEb7ff1",
            "tokenId": str(id)
        },
        "id": 1
    })
    headers = {}

    res = requests.request("POST", url, headers=headers, data=payload).json()

    bids = res["result"]["data"]
    if not bids:
        print(id, None)
        return {
            "id": id,
            "address": None,
            "username": None,
            "price": None,
            "star": None,
            "num": len(bids)
        }

    bid_adds = []

    for bid in bids:
        if bid["bidderAddress"] not in bid_adds:
            bid_adds.append(bid["bidderAddress"])

    bid_star = [address_star.get(address, 0) for address in bid_adds]
    max_star =  max(bid_star)

    bid = bids[0]
    price = int(bid["bidPrice"]) / 10**18
    address = bid["bidderAddress"]
    username = bid.get("bidderUserName")
    star = address_star.get(address)
    if star is None:
        star = get_user_token(address)
    # df = pd.read_csv("starverse_users.csv")
    # lookup = dict(zip(df["address"], df["username"]))
    print(id, username, price, star)
    return {
        "id": id,
        "address": address,
        "username": username,
        "price": price,
        "star": star,
        "num": len(bid_adds),
        "num_bid": len(bids),
        "max_star": max_star,
        "max_address": bid_adds[bid_star.index(max_star)]
    }

address_star = get_token_holders(3000)


item_bid = {}
items = []
for i in list(range(251, 501)) + list(range(751, 1001)):
    item = get_tshirt(i)
    if item["num"] == 0:
        continue

    items.append(item)
    a = item["address"]
    if a not in item_bid:
        item_bid[a] = []
    item_bid[a].append(item["price"]) 

for item in items:
    a = item["address"]
    item["num_tshirt"] = len(item_bid[a])
    item["total_star"] = sum(item_bid[a]) + item["star"]
    ma = item["max_address"]
    item["max_num_tshirt"] = len(item_bid[ma])
    item["max_total_star"] = sum(item_bid[ma]) + item["max_star"]

df = pd.DataFrame(items)
df.to_excel("tshirt_v5.xlsx", index=False, encoding="utf-8-sig")