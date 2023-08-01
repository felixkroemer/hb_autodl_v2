# TODO: check https://indefero.soutade.fr//p/libgourou/, https://www.e-reader-forum.de/t/calibre-plugin-fuer-acsm-epub-konvertierung.157575/

import os
import random
import re
import secrets
import string
import subprocess

import requests
from dotenv import load_dotenv


def main():
    load_dotenv()
    session = login()

    magazines = session.get(
        os.getenv("HOME_URL")
        + "/frontend/simpleMediaList,0-0-0-109-0-0-0-0-0-352189746-0.html"
    )

    newest_version_regex = re.compile('href="(mediaInfo,((\d+)-){10}(\d+)\.html)"')
    newest_version = newest_version_regex.search(str(magazines.content)).group(1)
    magazine_borrow = session.post(
        os.getenv("HOME_URL") + "/frontend/" + newest_version
    )
    acsm_regex = re.compile('href="(https://acs4\..*?)"')
    acsm_url = acsm_regex.search(str(magazine_borrow.content)).group(1)
    acsm = session.get(acsm_url)

    if acsm.status_code != 200:
        print("Error {}".format(acsm.status_code))
    else:
        path = os.path.join(
            os.environ["TMP"],
            "HB_{}.acsm".format(
                random.choices(string.ascii_uppercase + string.digits, k=16)
            ),
        )
        with open(path, "wb") as f:
            f.write(acsm.content)
        subprocess.Popen([path], shell=True)


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
