
import requests
import json
import string
from collections import Counter

def get_min_price(c, k=1, bid=False):
    url = "https://api.yoverse.io/marketplace/rpc"

    if c == "1":
        c_value = "26"
    elif c == "8":
        c_value = "27"
    else:
        c_value = str(ord(c) - 65)

    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "vmp_searchNFT",
        "params": {
            "saleTypes": [
                "ON_AUCTION" if bid else "BUY_NOW"
            ],
            "contractAddress": [
                "0xd390b879e73EB4F64E037Bd9a054995D7553FC65"
            ],
            "limit": 10,
            "sort": {
                "sortType": "price",
                "sortField": "PRICE_LOW_TO_HIGH",
                "sortCurrency": "STAR"
            },
            "attrs": [
                {
                    "traitType": "Character",
                    "value": [
                        c_value
                    ]
                }
            ]
        }
    })
    headers = {}

    res = requests.request("POST", url, headers=headers, data=payload).json()

    stars = []

    for a in res["result"]["data"][:k]:
        id = a["tokenID"]
        if bid:
            end = a["endedDate"]
            bprice =  a["priceBid"]["STAR"]
            price = -1
            if a["prices"]:
                price = a["prices"]["STAR"]

            stars.append((bprice, id, price))            
        else: 
            price = a["prices"]["STAR"]
            stars.append((price, id))            

    return stars


def get_text_price(text, bid=False):
    print(text)
    s = 0
    for c, k in sorted(Counter(text).items()):
        cs = get_min_price(c, k, bid)
        print(c, cs)
        s += sum([x[0] for x in cs])
    print(s)

if __name__ == "__main__":
    text = "EMBRACINGCHALLENGES"
    # text = "ADVANCINGPARTNERSHIP"
    # text = "UPHOLDINGINTEGRITY"
    texts = [
        # "EMBRACINGCHALLENGES",
        # "ADVANCINGPARTNERSHIP",
        # "UPHOLDINGINTEGRITY",
        # "HAPPYBIRTHDAYVNG18",
        string.ascii_uppercase
    ]

    have = "SGD" + "BDQEGPRYYK" + "MVP" + "SQKA" 
    have = ""
    print(sorted(have))
    for text in texts:
        raw = text
        for c in have:
            text = text.replace(c, "", 1)

        get_text_price(raw)
        # get_text_price(text)
        # get_text_price(text, True)
        