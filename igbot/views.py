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

from igbot.machine_params import machineSet

import io
from PIL import Image

post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN

machine = {}

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
        machine[send_id].advance(send_id, text)
    if state == "instadp":
        machine[send_id].instadp_next(send_id, text)
    if state == "instadpinput":
        machine[send_id].instadpinput_next(send_id, text)
    if state == "printinstadp":
        machine[send_id].printdp_next(send_id, text)
    if state == "lobby":
        machine[send_id].lobby_next(send_id, text)
    if state == "igviewer":
        machine[send_id].igviewer_next(send_id, text)
    if state == "iguploader":
        machine[send_id].iguploader_next(send_id, text)
    if state == "viewig":
        machine[send_id].view_next(send_id, text)

def show_fsm(self):
    if "graph" not in machine:
        machine["graph"] = TocMachine(
            states=machineSet["states"],
            transitions=machineSet["transitions"],
            initial=machineSet["initial"],
            auto_transitions=machineSet["auto_transitions"],
        )
    machine["graph"].get_graph().draw('fsm.png', prog='dot', format='png')
        
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
                if sender_id not in machine:
                    machine[sender_id] = TocMachine(
                        states=machineSet["states"],
                        transitions=machineSet["transitions"],
                        initial=machineSet["initial"],
                        auto_transitions=machineSet["auto_transitions"],
                    )
                handleTrigger(machine[sender_id].state, sender_id, text)
            return HttpResponse()
        else :
            return HttpResponse()

class InstagrammerViewSet(viewsets.ModelViewSet):
    queryset = Instagrammer.objects.all()
    serializer_class = InstagrammerSerializer

def login(request):
    return render(request, 'login.html')