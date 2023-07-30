import os
import secrets

import requests
from dotenv import load_dotenv


def main():
    load_dotenv()
    session = login()


def login():
    s = requests.session()
    resp = s.get("https://www.onleihe.de/metropolbib")
    tid = secrets.token_hex(32).upper()
    data = {
        "username": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "tid": tid,
        "log": "login",
        "libraryId": os.getenv("LIBRARY_ID"),
        "feld": 1,
        "aloFrm": 700013,
        "afepId": 700001,
        "devId": 0,
        "sid": s.cookies["JSESSIONID"] + ".tomcat8_2",
    }
    resp = s.post("https://" + os.getenv("LOGIN_URL") + "/" + tid, data=data)
    return s


if __name__ == "__main__":
    main()
