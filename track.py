import requests
from bs4 import BeautifulSoup
import time
import logging
import sys
import arrow
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="[%(asctime)s] - %(message)s")
import smtplib, ssl
from getpass import getpass
import os

WEB_URL = "https://www.apple.com/sg/shop/product/FTXP2ZP/A/Refurbished-11-inch-iPad-Pro-Wi-Fi-64GB-Silver"

API = "https://www.apple.com/sg/shop/delivery-message"

MESSAGE = """\
Subject: {part} is available.

{content}"""

class Ipad:
    def __str__(self):
        return f"Refurbished iPad {self.COLOR}"


class SpaceGrey(Ipad):
    TYPE = "FTXN2ZP/A"
    COLOR = "Space Grey"


class Silver(Ipad):
    TYPE = "FTXP2ZP/A"
    COLOR = "Silver"

PARTS_TO_TRACK = [SpaceGrey(), Silver()]


class Application:
    def __init__(self):
        self.port = 465  # For SSL
        self.email = os.environ.get("EMAIL") or input("Email: ")
        self.password = os.environ.get("EP") or getpass(prompt="Type your password and press enter: ")
        # Create a secure SSL context
        self.context = ssl.create_default_context()

    def send_email(self, message):
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
                server.login(self.email, self.password)

                server.sendmail(self.email, self.email, message)
                logging.info("EMAIL SENT")

    def run(self):
        while True:
            for part in PARTS_TO_TRACK:
                params = {"parts.0": part.TYPE}
                res = requests.get(API, params=params)

                if res.status_code != 200:
                    logging.error(f"API {API} error. {res.json()}")
                    continue

                res = res.json()
                is_available = self.parse_stock(res, part.TYPE)

                if not is_available:
                    logging.info(f"{part} still not available yet.")
                    continue
                else:
                    content = f"""
    Refurbished iPad Pro 11 inch {part.COLOR} is available!

    Link: {WEB_URL}
                    """
                    message = MESSAGE.format(content=content, part=part)
                    self.send_email(message)

            time.sleep(10)

    def parse_web(self, res):
        res = res.content.decode("utf-8")
        soup = BeautifulSoup(res, "html.parser")

        button = soup.find("button", {"type": "submit", "name": "add-to-cart"})
        button_cls = button.get("class")

        return not "disabled" in button_cls

    def parse_stock(self, json, part):
        part_info = json.get("body", {}).get("content", {}).get("deliveryMessage").get(part, {})
        is_buyable = part_info.get("isBuyable")
        delivery_msg = part_info.get("deliveryOptionMessages")
        if len(delivery_msg) > 0:
            msg = delivery_msg[0]

        return is_buyable or msg.lower() != "out of stock"


if __name__ == "__main__":
    app = Application()
    app.run()
