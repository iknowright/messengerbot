import requests
import re
import codecs
url = "https://www.instagram.com/{}"
r = requests.get(url.format("wshusen"))
html = r.text
print(re.findall('"profile_pic_url_hd":"(.*?)",', html)[0])
x = re.findall('"biography":"(.*?)",', html)[0]
x = re.sub(r'\\u([d][a-z|A-Z|0-9]{3})\\u([d][a-z|A-Z|0-9]{3})', u"\u26F6", x)
unicodes = re.findall(r'\\u([^d][a-z|A-Z|0-9]{3})', x)
normal = re.findall(r'\\[^u]', x)
import ast
s = x
for uni in unicodes:
    the_code = (r"u" + uni)
    the_code = u'\\{}'.format(the_code)
    print(the_code)
    thecode_bis = ast.literal_eval(u'u"'+ the_code + '"')
    print(thecode_bis)
    s = s.replace(the_code, thecode_bis)

ss = s
for norm in normal:
    thecode_bis = ast.literal_eval(u'u"'+ norm + '"')
    ss = ss.replace(norm, thecode_bis)

