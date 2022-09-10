import os
import json
import requests
import tqdm
import pandas as pd

def get_username(address):
    url = "https://api.yoverse.io/marketplace/rpc"

    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "vmp_getProfile",
        "params": {
            "walletAddress": address
        },
        "id": 1
    })
    headers = {}
    res = requests.request("POST", url, headers=headers, data=payload).json()

    return res["result"]["data"]["username"]

def get_token_holders(size=10):
    url = f"https://scan.testnet.verichains.xyz/api?module=token&action=getTokenHolders&contractaddress=0x82a29828a3B5c16ed13Dc7840D0699746D2a741C&offset={size}"

    payload = ""
    headers = {}

    res = requests.request("GET", url, headers=headers, data=payload).json()

    return res["result"]

def get_user(size=10):
    holders = get_token_holders(size)
    print(len(holders))
    for h in tqdm.tqdm(holders):
        h["star"] = int(h["value"])/10**18
        h["username"] = get_username(h["address"])
        h.pop("value")
    
    return holders

def update_user(size=3000):
    path = "starverse_users.csv"
    lookup = {}
    if os.path.exists(path):
        df = pd.read_csv(path)
        lookup = dict(zip(df["address"], df["username"]))
    
    holders = get_token_holders(size)
    print(len(holders))
    for h in tqdm.tqdm(holders):
        h["star"] = int(h["value"])/10**18
        h["username"] = lookup.get(h["address"])
        if not h["username"]:
            h["username"] = get_username(h["address"])
        h.pop("value")

    df = pd.DataFrame(holders)
    df.to_csv(path, encoding="utf-8-sig", index=False)
    
    return df

if __name__ == "__main__":
    pd.options.display.max_rows = 3000
    df = update_user()
    print(len(df))
    print(sum(list(df["star"])[6:]))
    print(df.head(3000))