from transitions.extensions import GraphMachine
from igbot.messageAPI import MessageAPI
from igbot.models import Instagrammer

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state1(self, event):
        print("Testing State 1")
        # if event.get('message'):
        #     if event['message'].get('text'):
        #         text = event['message']['text']
        #         print("text:" + text)
        #         return text.lower() == 'go to state1'
        return False

    def is_going_to_state2(self, event):
        print("Testing State 2")       
        # if event.get('message'):
        #     if event['message'].get('text'):
        #         text = event['message']['text']
        #         print("text:" + text)
        #         return text.lower() == 'go to state2'
        return False

    def on_enter_state1(self, event):
        print("I'm entering state1")

        sender_id = event['sender']['id']
        api = MessageAPI(sender_id)
        # responese = api.text_message("I'm entering state1")
        api.profileTemplates(3)
        self.go_back()

    def on_exit_state1(self):
        print('Leaving state1')

    def on_enter_state2(self, event):
        print("I'm entering state2")

        sender_id = event['sender']['id']
        api = MessageAPI(sender_id)
        responese = api.text_message("I'm entering state2")
        self.go_back()

    def on_exit_state2(self):
        print('Leaving state2')