# import argparse
# import re
# import sys

# import requests


# # spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

# from imgurpython import ImgurClient
# from igbot.igbot_setting import *
# import json

# def getID(username):
#     url = "https://www.instagram.com/{}"

#     r = requests.get(url.format(username))

#     html = r.text
#     if r.ok:
#         return re.findall('"id":"(.*?)",', html)[0]

#     else:
#         print("\033[91m✘ Invalid username\033[0m")
#         return ""


# def fetchDP(userID):
#     url = "https://i.instagram.com/api/v1/users/{}/info/"

#     r = requests.get(url.format(userID))
#     print(r.status_code)
#     if r.ok:
#         print(r.json)
#         data = r.json()
#         return data['user']['hd_profile_pic_url_info']['url'], data['user']['biography']

#     else:
#         print("\033[91m✘ Cannot find user ID \033[0m")
#         return "",""

# def getImageUrl(instagram_id):
#     username = instagram_id

#     user_id = getID(username)
#     print(user_id)
#     if not user_id:
#         return "", ""
#     file_url, biography = fetchDP(user_id)
#     if not file_url:
#         return "", ""
#     fname = username + ".jpg"

#     r = requests.get(file_url, stream=True)
#     if r.ok:
#         n = requests.post("https://api.imgur.com/3/image", headers={"Authorization": "Bearer %s" % IMGUR_ACCESS_TOKEN}, data={"image":r.content})
#         response = n.json()
#         return response['data']['link'], biography
#     else:
#         print("Cannot make connection to download image")
#         return "", ""
from bs4 import BeautifulSoup
import requests
import re
def getImageUrl(instagram_id):
    url = "https://www.instagram.com/{}"
    r = requests.get(url.format(instagram_id))
    html = r.text
    return re.findall('"profile_pic_url_hd":"(.*?)",', html)[0], re.findall('"biography":"(.*?)",', html)[0]