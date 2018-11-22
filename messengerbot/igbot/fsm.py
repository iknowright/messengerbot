from transitions.extensions import GraphMachine
from igbot.messageAPI import MessageAPI
from igbot.models import Instagrammer
from igbot.messages import *
class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    # advance[]
    def is_going_to_instadp(self, sender_id, text):
        print("Testing Instadp")
        # return False
        return text == "instadp"


    def is_going_to_intro(self, sender_id, text):
        print("Testing State 1")
        # return False
        return text == "go to intro"

    def is_going_to_state2(self, sender_id, text):
        print("Testing State 2")
        # return False        
        return text == "go to intro"

    # state2
    def on_enter_intro(self, sender_id, text):
        print("I'm entering intro")
        api = MessageAPI(sender_id)
        # api.text_message("I'm entering intro")
        # api.profileTemplates(10)
        api.quickreply_message()
        self.go_back()

    def on_exit_intro(self):
        print('Leaving intro')

    # state2
    def on_enter_state2(self, sender_id, text):
        print("I'm entering state2")
        api = MessageAPI(sender_id)
        responese = api.text_message("I'm entering state2")
        self.go_back()

    def on_exit_state2(self):
        print('Leaving state2')

    # instadp
    def on_enter_instadp(self, sender_id, text):
        api = MessageAPI(sender_id)
        api.quickreply_message(messages['instadp_intro'], messages['instadp_intro_quickreply'])
        print(self.state)
        self.go_back()
