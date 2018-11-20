from igbot.igbot_setting import *
import requests
import json
post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN

class MessageAPI:
    def __init__(self, fb_id):
        self.fb_id = fb_id

    def text_message(self, content):
        response_msg = json.dumps({"recipient": {"id": self.fb_id}, "message": {"text": content}})
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response_msg)