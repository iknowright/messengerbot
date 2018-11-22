from igbot.igbot_setting import *
import requests
import json
from igbot.models import Instagrammer
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

    def quickreply_message(self):
        response = json.dumps({
            "recipient":{
                "id":self.fb_id
            },
            "message":{
                "text": "What u gonna do!",
                "quick_replies":[
                    {
                        "content_type":"location"
                    },
                    {
                        "content_type":"text",
                        "title":"看正妹",
                        "payload":"看正妹"
                    },
                    {
                        "content_type":"text",
                        "title":"新增正妹",
                        "payload":"新增正妹"
                    }
                ]
            }  
        })
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response)

    def profileTemplates(self, num):
        igs = Instagrammer.objects.all()[:num]
        generic_template = []
        for ig in igs:
            generic_template.append({
                "title":ig.id,
                "image_url":ig.image_url,
                # "subtitle":"",
                "default_action": {
                    "type": "web_url",
                    "url": ig.url,
                    "webview_height_ratio": "full",
                },
                "buttons":[
                    {
                        "type":"web_url",
                        "url":ig.url,
                        "title":"View Website",
                    },
                    {
                        "type": "postback",
                        "title": "Like",
                        "payload": "Like %s"%ig.id,
                    },
                ]      
            })
        print(generic_template)
        request = json.dumps({
            "recipient":{
            "id":self.fb_id
            },
            "message":{
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"generic",
                        "image_aspect_ratio":"square",
                        "elements": generic_template          
                    }
                }
            }
        })
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=request)