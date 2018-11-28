from igbot.instadp import *
import csv

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messengerbot.settings')
django.setup()

from igbot.models import Instagrammer

Instagrammer.objects.all().delete()

entries = [
    "stilleecho,清純,臺灣",
    "cherry_quahst,模特兒,馬來西亞",
    "wshusen,Youtuber,馬來西亞",
    "berryying,模特兒,泰國",
    "rockchaeeun,模特兒,韓國",
    "qiuwen1014,模特兒,馬來西亞",
    "bbooxlok,空姐,香港",
    "naomineo_,模特兒,新加坡",
    "wanna._b,模特兒,韓國",
    "yuviaxtsayx,空姐,臺灣",
]
for entry in entries: 
    # parsing each column of a row 
    textlist = entry.split(',')
    print (entry)
    image_url, bio = getImageUrl(textlist[0])
    if image_url == "":
        print("Id not found")
    else:
        print("processing %s"%textlist[0])
        Instagrammer.objects.create(
            id = textlist[0],
            genre = textlist[1],
            country = textlist[2],
            content = bio,
            url = "https://www.instagram.com/%s" % id,
            image_url = image_url
        )