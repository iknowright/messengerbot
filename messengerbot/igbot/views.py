from django.shortcuts import render
from django.http.response import HttpResponse

from igbot.igbot_setting import *
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests

post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN

# Handle messages events
def handleMessage(sender_psid, received_message):
    # Check if the message contains text
    if received_message.get('text'):
        # Create the payload for a basic text message
        response = {
            "text": "You sent the message: "+received_message["text"]+". Now send me an image!"
        }
        # Sends the response message
        callSendAPI(sender_psid, response)    
    return

# Handles messaging_postbacks events
def handlePostback(sender_psid, received_postback):
    pass

# Sends response messages via the Send API
def callSendAPI(sender_psid, response):
    # Construct the message body
    request_body = json.dumps({
        'recipient': {
        'id': sender_psid
        },
        'message': response
    })
    r = requests.post(post_url, headers={'Content-Type': 'application/json'}, data=request_body)
    print("<-------------Start of Response------------->")
    print(r.json())
    print("<-------------End of Response------------->")


# Create your views here.

class IgBotView(generic.View):
    # To callback Webhook, the only GET request that webhook sent to here 
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    # Prevent getting csrf error
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
            
    def post(self, request, *args, **kwargs):
        body = json.loads(self.request.body.decode('utf-8'))
        # print (body)
        if body['object'] == 'page': 
            for entry in body['entry']:
                # Get the webhook event. entry.messaging is an array, but 
                # will only ever contain one event, so we get index 0

                # Gets the body of the webhook event
                webhook_event = entry['messaging'][0]
                print("<-------------Start of Githook Content------------->")
                print(webhook_event)
                print("<-------------Start of Githook Content------------->")

                # Get the sender PSID
                sender_psid = webhook_event['sender']['id']

                if webhook_event.get('message'):
                    try:
                        handleMessage(sender_psid, webhook_event['message'])
                    except:
                        return HttpResponse(status=404)
                elif webhook_event.get('postback'):
                    try:
                        handlePostback(sender_psid, webhook_event['message'])
                    except:
                        return HttpResponse(status=404)
                
            return HttpResponse(status=200)
        else :
            return HttpResponse(status=404)