from django.shortcuts import render
from django.http.response import HttpResponse

from igbot.igbot_setting import *
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests

from igbot.messageAPI import MessageAPI
from igbot.fsm import TocMachine

post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN

machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

# Handle messages events
def handleMessage(sender_psid, received_message):
    sender = MessageAPI(sender_psid)

    # Check if the message contains text
    if received_message.get('text'):
        # Create the payload for a basic text message
        # sender.text_message(received_message['text'])
        sender.quickreply_message(received_message['text'])
        return
    elif received_message.get('attachments'):
        # Get the URL of the message attachment
        attachment_url = received_message['attachments'][0]['payload']['url']
        sender.image_message(attachment_url)
    return


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
                print("<-------------Start of Githook Content------------->")
                print(entry)
                print("<-------------End of Githook Content------------->")

                # Gets the body of the webhook event
                if entry.get('messaging'):
                    webhook_event = entry['messaging'][0]
                    # Get the sender PSID
                    sender_psid = webhook_event['sender']['id']

                    if webhook_event.get('message'):
                        try:
                            handleMessage(sender_psid, webhook_event['message'])
                        except:
                            return HttpResponse()
                    elif webhook_event.get('postback'):
                        try:
                            handlePostback(sender_psid, webhook_event['postback'])
                        except:
                            return HttpResponse()
            return HttpResponse()
        else :
            return HttpResponse()