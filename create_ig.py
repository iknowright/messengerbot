from igbot.instadp import *
import csv

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messengerbot.settings')
django.setup()

from igbot.models import Instagrammer


entries = [
    "andy_blossom,模特兒,臺灣",
    "mengj215,模特兒,臺灣",
    "juliamisakii,模特兒,臺灣",
    "lynnwu0219,模特兒,臺灣",
    "et.1231,模特兒,臺灣",
    "melody908yen,模特兒,臺灣",
    "chiaochiaotzeng,模特兒,臺灣",
    "jyjosephine,模特兒,馬來西亞",
    "serene_serenity,模特兒,馬來西亞",
    "yumiwong_official,模特兒,馬來西亞",
    "lavellaangel,模特兒,馬來西亞",
    "crystal_swung,模特兒,馬來西亞",
    "yingxuange,模特兒,臺灣",
    "dewichien,模特兒,臺灣",
    "kininii,模特兒,臺灣",
    "imjennycheng,模特兒,臺灣",
    "mayj517,模特兒,韓國    ",
    "berlin.ng,模特兒,新加坡",
]
for entry in entries: 
    # parsing each column of a row 
    textlist = entry.split(',')
    print (entry)
    image_url, bio = getImageUrl(textlist[0])
    print("processing %s"%textlist[0])
    Instagrammer.objects.create(
        id = textlist[0],
        genre = textlist[1],
        country = textlist[2],
        content = bio,
        url = "https://www.instagram.com/%s" % textlist[0],
        image_url = image_url
    )