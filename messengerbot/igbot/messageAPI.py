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

    def image_message(self, content):
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Pictures",
                        "subtitle": "Tap a button to answer.",
                        "image_url": content,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Yes!",
                                "payload": "yes",
                            },
                            {
                                "type": "postback",
                                "title": "No!",
                                "payload": "no",
                            }
                        ],
                    }]
                }
            }
        }
        response_msg = json.dumps({"recipient": {"id": self.fb_id}, "message": response})
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response_msg)

    def quickreply_message(self, content):
        response = json.dumps({
            "recipient":{
                "id":self.fb_id
            },
            "message":{
                "text": "Here is a quick reply!",
                "quick_replies":[
                    {
                        "content_type":"location"
                    }
                ]
            }  
        })
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response)