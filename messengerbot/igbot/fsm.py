from transitions.extensions import GraphMachine
from igbot.messageAPI import MessageAPI
from igbot.models import Instagrammer
from igbot.messages import *
from igbot.instadp import *

singleIgUrl = ""

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
        self.set_single_url()

    # set_single_url
    def set_single_url(self, ig_id = "",url = ""):
        self.url = url
        self.ig_id = ig_id
    
    def get_single_url(self):
        return self.ig_id, self.url

    # ----------------Conditions--------------------
    # advance
    def say_instadp(self, sender_id, text):
        print("Testing Instadp")
        return text == "instadp"

    def say_intro(self, sender_id, text):
        print("Testing Intro")
        return text != "instadp"

    # instadp_next
    def press_start(self, sender_id, text):
        print("Testing press_start")
        print(text)
        
        return text == "開始"

    def press_return(self, sender_id, text):
        print("Testing press_return")
        return text == "返回"

    # instadpinput_next
    def valid_id(self, sender_id, text):
        print("Testing valid_id")
        print(text)
        image_url, bio = getImageUrl(text)
        self.set_single_url(text, image_url)
        print(image_url)
        return image_url != ""

    def invalid_id(self, sender_id, text):
        print("Testing invalid_id")
        print(text)
        image_url, bio = getImageUrl(text)
        print(image_url)
        return image_url == ""

    # printdp_next
    def press_upload(self, sender_id, text):
        return text == "上傳"

    def press_again(self, sender_id, text):
        return text == "再一張"


    # ----------------States--------------------
    

    # intro
    def on_enter_intro(self, sender_id, text):
        print("I'm entering intro")
        api = MessageAPI(sender_id)
        self.go_back()

    # instadp
    def on_enter_instadp(self, sender_id, text):
        api = MessageAPI(sender_id)
        api.quickreply_message(messages['instadp'], messages['instadp_quickreply'])

    # instadp_input
    def on_enter_instadpinput(self, sender_id, text):
        api = MessageAPI(sender_id)
        print(text)
        api.quickreply_message(messages['instadpinput'], messages['instadpinput_quickreply'])

    # printinstadp
    def on_enter_printinstadp(self, sender_id, text):
        api = MessageAPI(sender_id)
        ig_id, url = self.get_single_url()
        api.image_message(url)
        api.quickreply_message("想要貢獻給大衆嗎？\n點擊上傳，將ID分享至伺服器\n點擊再一張，獲取新的一張", messages['printdp_quickreply'])

    # instadperror
    def on_enter_instadperror(self, sender_id, text):
        api = MessageAPI(sender_id)
        print(text)
        api.text_message("IG使用者ID有誤，請重新輸入")
        self.gobackinput(sender_id, text)

    # instadperror
    def on_enter_printdpserver(self, sender_id, text):
        api = MessageAPI(sender_id)
        ig_id, url = self.get_single_url()
        entry = Instagrammer.objects.filter(id = ig_id)
        if entry.exists():
            api.text_message("資料已經在資料庫了，棒棒的，看來妹子很有名～")
        else:
            Instagrammer.objects.create(
                id = ig_id,
                genre = "",
                country = "",
                content = "",
                url = "https://www.instagram.com/%s" % ig_id,
                image_url = url
            )
        entry = Instagrammer.objects.get(id = ig_id)
        api.text_message("IG上傳成功")
        api.profileTemplatesSingle(entry)
        self.gobackinput(sender_id, text)