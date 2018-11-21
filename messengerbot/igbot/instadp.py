#!/usr/bin/env python3

import argparse
import re
import sys

import requests


# spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

from imgurpython import ImgurClient
import json

# If you already have an access/refresh pair in hand
client_id = '3c54f578350162a'
client_secret = '540119cbb8118d81f4e6677162d47098d940e93d'
access_token = '77189f5c5b15f963388b2a054c23ca38521e68ae'
refresh_token = '166066836f65a4df97b922e29bdaaadcbb597e47'

# Note since access tokens expire after an hour, only the refresh token is required (library handles autorefresh)
client = ImgurClient(client_id, client_secret, access_token, refresh_token)


def getID(username):
    url = "https://www.instagram.com/{}"

    r = requests.get(url.format(username))

    html = r.text

    if r.ok:
        return re.findall('"id":"(.*?)",', html)[0]

    else:
        print("\033[91m✘ Invalid username\033[0m")
        sys.exit()


def fetchDP(userID):
    url = "https://i.instagram.com/api/v1/users/{}/info/"

    r = requests.get(url.format(userID))

    if r.ok:
        data = r.json()
        return data['user']['hd_profile_pic_url_info']['url']

    else:
        print("\033[91m✘ Cannot find user ID \033[0m")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(
        description="Download any users Instagram display picture/profile picture in full quality")

    parser.add_argument('username', action="store", help="username of the Instagram user")

    args = parser.parse_args()

    username = args.username

    user_id = getID(username)
    file_url = fetchDP(user_id)
    fname = username + ".jpg"

    r = requests.get(file_url, stream=True)
    if r.ok:
        with open(fname, 'wb') as f:
            n = requests.post("https://api.imgur.com/3/image", headers={"Authorization": "Bearer %s" % access_token}, data={"image":r.content})
            response = n.json()
            print(response)
            

            print("\033[92m✔ File save:\033[0m {}".format(fname))
    else:
        print("Cannot make connection to download image")


if __name__ == "__main__":
    main()
