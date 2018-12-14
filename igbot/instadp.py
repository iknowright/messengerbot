import requests
import re
def getImageUrl(instagram_id):
    url = "https://www.instagram.com/{}"
    r = requests.get(url.format(instagram_id))
    html = r.text
    return re.findall('"profile_pic_url_hd":"(.*?)",', html)[0], re.findall('"biography":"(.*?)",', html)[0]