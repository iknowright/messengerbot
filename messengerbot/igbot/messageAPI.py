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

    def image_message(self, image_url):
        response = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable":True
                }
            }
        }
        response_msg = json.dumps({"recipient": {"id": self.fb_id}, "message": response})
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response_msg)

    def quickreply_message(self, text, quickreply):
        response = json.dumps({
            "recipient":{
                "id":self.fb_id
            },
            "message":{
                "text": text,
                "quick_replies":quickreply
            }  
        })
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response)
    
    def button_message(self, text, button):
        response = json.dumps({
            "recipient":{
                "id":self.fb_id
            },
            "message":{
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":text,
                        "buttons":button
                    }
                }
            }
        })
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response)

    def profileTemplates(self, entries):
        entries = entries[:10]
        generic_template = []
        for ig in entries:
            title = ig.id
            if not ig.genre or ig.genre != "無":
                title = "%s %s" % (title, ig.genre)
            if not ig.country or ig.country != "無":
                title = "%s %s" % (title, ig.country)
            generic_template.append({
                "title":title,
                "image_url":ig.image_url,
                "subtitle":"%s..." % ig.content[:76],
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
                        "payload": "payload_like %s"%ig.id,
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

    def profileTemplatesSingle(self, ig):
        title = ig.id
        if not ig.genre or ig.genre != "無":
            title = "%s %s" % (title, ig.genre)
        if not ig.country or ig.country != "無":
            title = "%s %s" % (title, ig.country)
        generic_template = [
            {
                "title": title,
                "image_url":ig.image_url,
                "subtitle":"%s..."%ig.content[:76],
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
                        "payload": "payload_like %s"%ig.id,
                    },
                ]      
            }
        ]
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

    def quickreply_button_message(self, text, quickreply, button):
        response = json.dumps({
            "recipient":{
                "id":self.fb_id
            },
            "message":{
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":text,
                        "buttons":button
                    }
                },
                "quick_replies":quickreply
            }
        })
        requests.post(post_url, headers={"Content-Type": "application/json"}, data=response)