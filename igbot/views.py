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
from igbot.models import Instagrammer
from igbot.serializers import InstagrammerSerializer

from rest_framework import viewsets

post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN

machine = TocMachine(
    states=[
        'user',
        'lobby',
        'instadp',
        'instadpinput',
        'printinstadp',
        'instadperror',
        'printdpserver',
        'igviewer',
        'iguploader',
        'viewig',
        'uploadprocess'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'lobby',
        },
        {
            'trigger': 'instadp_next',
            'source': 'instadp',
            'dest': 'instadpinput',
            'conditions': 'press_start'
        },
        {
            'trigger': 'instadp_next',
            'source': 'instadp',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'instadpinput_next',
            'source': 'instadpinput',
            'dest': 'printinstadp',
            'conditions': 'valid_id'
        },
        {
            'trigger': 'instadpinput_next',
            'source': 'instadpinput',
            'dest': 'instadperror',
            'conditions': 'invalid_id'
        },
        {
            'trigger': 'gobackinput',
            'source': 'instadperror',
            'dest': 'instadpinput',
        },
        {
            'trigger': 'instadpinput_next',
            'source': 'instadpinput',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'printdp_next',
            'source': 'printinstadp',
            'dest': 'instadpinput',
            'conditions': 'press_again'
        },
        {
            'trigger': 'printdp_next',
            'source': 'printinstadp',
            'dest': 'printdpserver',
            'conditions': 'press_upload'
        },
        {
            'trigger': 'gobackinput',
            'source': 'printdpserver',
            'dest': 'instadpinput',
        },
        {
            'trigger': 'lobby_next',
            'source': 'lobby',
            'dest': 'instadp',
            'conditions': 'is_instadp'
        },
        {
            'trigger': 'lobby_next',
            'source': 'lobby',
            'dest': 'iguploader',
            'conditions': 'is_contribute'
        },
        {
            'trigger': 'lobby_next',
            'source': 'lobby',
            'dest': 'igviewer',
            'conditions': 'is_view'
        },
        {
            'trigger': 'igviewer_next',
            'source': 'igviewer',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'iguploader_next',
            'source': 'iguploader',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'igviewer_next',
            'source': 'igviewer',
            'dest': 'viewig',
            'conditions': 'not_return'
        },
        {
            'trigger':'gobackupload',
            'source': 'uploadprocess',
            'dest': 'iguploader',
        },
        {
            'trigger': 'iguploader_next',
            'source': 'iguploader',
            'dest': 'uploadprocess',
        },
        {
            'trigger': 'view_next',
            'source': 'viewig',
            'dest': 'viewig',
            'conditions': 'not_return'
        },
        {
            'trigger': 'view_next',
            'source': 'viewig',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
    ],
    initial='user',
    auto_transitions=False,
)

# Handle messages events
def handleMessage(event):
    # Check if the message contains text
    text = ""
    if event.get('message'):
        if event['message'].get('text'):
            text = event['message']['text']
    elif event.get('postback'):
        if event['postback'].get('payload'):
            text = event['postback']['payload']
    return text

# Handle State Trigger
def handleTrigger(state, send_id, text):
    print("Server Handling State : %s" % state)
    if state == "user":
        machine.advance(send_id, text)
    if state == "instadp":
        machine.instadp_next(send_id, text)
    if state == "instadpinput":
        machine.instadpinput_next(send_id, text)
    if state == "printinstadp":
        machine.printdp_next(send_id, text)
    if state == "lobby":
        machine.lobby_next(send_id, text)
    if state == "igviewer":
        machine.igviewer_next(send_id, text)
    if state == "iguploader":
        machine.iguploader_next(send_id, text)
    if state == "viewig":
        machine.view_next(send_id, text)

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
            # Get the webhook event. entry.messaging is an array, but 
            # will only ever contain one event, so we get index 0
            print("\n\n<-------------Start of Githook Content------------->")
            print(body)
            print("<-------------End of Githook Content------------->")
            entry = body['entry'][0]
            # Gets the body of the webhook event
            if entry.get('messaging'):
                webhook_event = entry['messaging'][0]
                text = handleMessage(webhook_event)
                sender_id = webhook_event['sender']['id']

                handleTrigger(machine.state, sender_id, text)
            return HttpResponse()
        else :
            return HttpResponse()

class InstagrammerViewSet(viewsets.ModelViewSet):
    queryset = Instagrammer.objects.all()
    serializer_class = InstagrammerSerializer