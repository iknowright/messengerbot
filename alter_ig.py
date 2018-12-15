from igbot.instadp import *
import csv

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messengerbot.settings')
django.setup()

from igbot.models import Instagrammer

entries = Instagrammer.objects.all()
for entry in entries: 
    # parsing each column of a row 
    textlist = entry.split(',')
    print (entry)
    image_url, bio = getImageUrl(textlist[0])
    # we know bio is wrong , now fix it 

    # clean up the emoji change it to rectangle, since emoji not supported
    bio = re.sub(r'\\u([d][a-z|A-Z|0-9]{3})\\u([d][a-z|A-Z|0-9]{3})', u"\u26F6", bio)
    # get remaining unicode
    unicodes = re.findall(r'\\u([^d][a-z|A-Z|0-9]{3})', x)
    # use magic library to fix
    import ast
    s = x
    for uni in unicodes:
        the_code = (r"u" + uni)
        the_code = u'\\{}'.format(the_code)
        print(the_code)
        # magic here
        thecode_bis = ast.literal_eval(u'u"'+ the_code + '"')
        print(thecode_bis)
        # replace the unicode with correct character
        s = s.replace(the_code, thecode_bis)
    
    print("processing %s"%textlist[0])
    Instagrammer.objects.create(
        id = textlist[0],
        genre = textlist[1],
        country = textlist[2],
        content = s,
        url = "https://www.instagram.com/%s" % textlist[0],
        image_url = image_url
    )