import logging
import os

import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))

PRODUCT_URL = os.getenv("PRODUCT_URL", "https://www.keychron.com/products/low-profile-abs-full-set-keycap-set?variant=40332974981209")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def send_notification(message: str):
    print(message)
    if not WEBHOOK_URL:
        return
    requests.post(WEBHOOK_URL, json={"content": message})


def check_stock():
    resp = requests.get(PRODUCT_URL)
    if resp.status_code != 200:
        print(resp.status_code)
        return
    soup = BeautifulSoup(resp.content.decode(), 'html.parser')
    results = soup.find_all("meta", {"property": "omega:product"})
    if not results:
        print("Unable to find product ID!")
        return
    product_id = results[0]['content']
    results = soup.find_all("span", id=f"AddToCartText-{product_id}")
    if not results:
        print("Could not find button text")
        return
    if "sold out" in results[0].text.lower():
        print("Sold Out!")
        return False
    send_notification(f"Product Available!\n\n{PRODUCT_URL}")
    return True


def main():
    if not check_stock():
        exit(1)


if __name__ == '__main__':
    main()
