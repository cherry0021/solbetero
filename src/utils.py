from loguru import logger
import random
import time
import os
import requests
def sleep_random(min_time, max_time):
    delay = random.uniform(min_time, max_time)
    logger.debug(f"Sleeping for {delay} seconds")
    time.sleep(delay)

def load_proxy():
    with open(os.path.join(os.getcwd(), "proxies.txt"), "r") as file:
        lines = file.read().splitlines()
        if len(lines) == 0:
            raise Exception("No proxies found in proxies.txt")
        proxy_split = random.choice(lines).split(":")
        if len(proxy_split) == 2:
            return {
                "ip": proxy_split[0], 
                "port": int(proxy_split[1])
            }
        else:
            return {
                "ip": proxy_split[0], 
                "port": int(proxy_split[1]),
                "user": proxy_split[2], 
                "pass": proxy_split[3]
            }
def get_enumproxy():
    url = "https://ephemeral-proxies.p.rapidapi.com/v2/datacenter/proxy"
    querystring = {"countries": 'GB'}
    headers = {
        "X-RapidAPI-Key": "60f7bdf787msh61ddbd43812c12cp1059a4jsnd4564938be2c",
        "X-RapidAPI-Host": "ephemeral-proxies.p.rapidapi.com"}

    goodproxy = None
    while not goodproxy:
        print("fetching new proxy...")
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        print(response)
        req = requests.Session()
        host = response["proxy"]["host"]
        port = response["proxy"]["port"]
        proxies = f"http://{host}:{port}"
        req.proxies = {"http": proxies,
                       "https": proxies}
        res = req.request("GET", "http://ipinfo.io/ip", headers=headers)
        if res.status_code == 200:
            print(res.text)
            goodproxy = True
            print("fetching done.. proxy is good now.")
            return host, port
        else:
            goodproxy = False
            return False