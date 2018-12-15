import requests
import re
def getImageUrl(instagram_id):
    url = "https://www.instagram.com/{}"
    r = requests.get(url.format(instagram_id))
    html = r.text
    img_url = re.findall('"profile_pic_url_hd":"(.*?)",', html)
    bio = re.findall('"biography":"(.*?)",', html)
    if img_url is None:
        return "", ""
    else :
        return img_url[0], bio[0]
        