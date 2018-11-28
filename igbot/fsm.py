from transitions.extensions import GraphMachine
from igbot.messageAPI import MessageAPI
from igbot.models import Instagrammer
from igbot.messages import *
from igbot.instadp import *

from igbot.igbot_setting import *
import operator
singleIgUrl = ""
post_url = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=%s" % ACCESS_TOKEN

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
        self.set_single_url()

    # set_single_url
    def set_single_url(self, ig_id = "",url = "", bio = ""):
        self.url = url
        self.bio = bio
        self.ig_id = ig_id
    
    def get_single_url(self):
        return self.ig_id, self.url

    def set_command(self, valid = False):
        self.valid = valid

    def get_command(self):
        return self.valid

    # ----------------Conditions--------------------
    # advance
    def is_instadp(self, sender_id, text):
        print("Testing Instadp")
        return text.lower() == "instadp"

    def is_view(self, sender_id, text):
        print("Testing View")
        return text.lower() == "view"

    def is_contribute(self, sender_id, text):
        print("Testing Contribute")
        return text.lower() == "contribute"

    # printdp_next
    def press_upload(self, sender_id, text):
        return text == "上傳"

    def press_again(self, sender_id, text):
        return text == "再一張"

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
        self.set_single_url(text, image_url, bio)
        print(image_url)
        return image_url != ""

    def invalid_id(self, sender_id, text):
        print("Testing invalid_id")
        print(text)
        image_url, bio = getImageUrl(text)
        print(image_url)
        return image_url == "" and text != "返回"

    def not_return(self, sender_id, text):
        return text != '返回'

    # ----------------States--------------------

    # Lobby
    def on_enter_lobby(self, sender_id, text):
        api = MessageAPI(sender_id)
        api.button_message(messages['lobby'], messages['lobby_button'])
    
    # instadp
    def on_enter_instadp(self, sender_id, text):
        api = MessageAPI(sender_id)
        api.button_message(messages['instadp'], messages['instadp_button'])

    # instadp_input
    def on_enter_instadpinput(self, sender_id, text):
        api = MessageAPI(sender_id)
        print(text)
        api.quickreply_button_message(messages['instadpinput'], messages['instadpinput_quickreply'], messages['returnlobby_button'])

    # printinstadp
    def on_enter_printinstadp(self, sender_id, text):
        api = MessageAPI(sender_id)
        ig_id, url = self.get_single_url()
        api.image_message(url)
        api.button_message("想要貢獻給大衆嗎？\n點擊上傳，將ID分享至伺服器\n點擊再一張，獲取新的一張", messages['printdp_button'])

    # instadperror
    def on_enter_instadperror(self, sender_id, text):
        api = MessageAPI(sender_id)
        print(text)
        api.text_message("IG使用者ID有誤，請重新輸入")
        self.gobackinput(sender_id, text)

    # instadperror
    def on_enter_printdpserver(self, sender_id, text):
        api = MessageAPI(sender_id)
        ig_id, url, bio = self.get_single_url()
        entry = Instagrammer.objects.filter(id = ig_id)
        if entry.exists():
            api.text_message("資料已經在資料庫了，棒棒的，看來妹子很有名～")
        else:
            Instagrammer.objects.create(
                id = ig_id,
                genre = "",
                country = "",
                content = bio,
                url = "https://www.instagram.com/%s" % ig_id,
                image_url = url
            )
            api.text_message("IG上傳成功")
        entry = Instagrammer.objects.get(id = ig_id)
        api.profileTemplatesSingle(entry)
        self.gobackinput(sender_id, text)

    # Igviewer
    def on_enter_igviewer(self, sender_id, text):
        api = MessageAPI(sender_id)
        alldata = Instagrammer.objects.all()
        totalnumber = len(alldata)
        genres = Instagrammer.objects.order_by('genre').values('genre').distinct()
        genrelist = ""
        for entry in genres:
            if not entry['genre'] or entry['genre'] != '無':
                genrelist = "%s\n%s" % (genrelist,entry['genre'])
        countries = Instagrammer.objects.order_by('country').values('country').distinct()
        countrylist = ""
        for entry in countries:
            if not entry['country'] or entry['country'] != '無':
                countrylist = "%s\n%s" % (countrylist, entry['country'])
        print(genrelist)
        print(countrylist)
        api.button_message("目前資料庫共有 %d 資料!\n輸入搜尋關鍵字\n\"我要看[關鍵字]正妹\"\n\n特殊關鍵字[一項]:\n熱門（Order By Likes)\n最新(Order By Create Date)\n\n類別關鍵字[一項]:%s\n國家關鍵字[一項]:%s" % (totalnumber, genrelist, countrylist), messages['returnlobby_button'])        
        api.quickreply_message("範例 \"我要看馬來西亞正妹\" \"我要看最新空姐正妹\" \"我要看臺灣模特兒正妹\"", messages['viewig_quickreply'])

    # Iguploader
    def on_enter_iguploader(self, sender_id, text):
        api = MessageAPI(sender_id)
        api.button_message("上傳格式: ig_id [分類] [國家] \n（以空白爲分割，中括號爲選項)\n 例: changchaishi 小編 臺灣", messages['returnlobby_button'])
        
    def on_enter_viewig(self, sender_id, text):
        api = MessageAPI(sender_id)
        textlist = text.split(' ')
        if textlist[0] == "payload_like":
            liked_entry = Instagrammer.objects.get(id=textlist[1])
            liked_entry.likes += 1
            liked_entry.save()
            api.text_message("You Liked %s, Now %dLikes "%(textlist[1],liked_entry.likes))
            api.quickreply_button_message("範例 \"我要看馬來西亞正妹\" \"我要看最新空姐正妹\" \"我要看臺灣模特兒正妹\"", messages['viewig_quickreply'],messages['returnlobby_button'])            
        elif len(text) < 5 or not (text[0] == '我' and text[1] == '要' and text[2] == '看' and text[-2] == '正' and text[-1] == '妹'):
            api.text_message("格式錯誤請重新再試")
        else:
            genres = Instagrammer.objects.order_by('genre').values('genre').distinct()
            countries = Instagrammer.objects.order_by('country').values('country').distinct()
            genre_taken = ""
            country_taken = ""
            keyword = ""
            genreflag = False
            countryflag = False
            for entry in genres:
                r = text.find(entry['genre'])
                if r > 0 and genreflag is False:
                    genreflag = True
                    genre_taken = entry['genre']
                    r_genre = r
            for entry in countries:
                r = text.find(entry['country'])
                if r > 0 and countryflag is False:
                    countryflag = True
                    country_taken = entry['country']
                    r_country = r
            filterig = Instagrammer.objects.all()
            if genre_taken and not country_taken:
                filterig = filterig.filter(genre = genre_taken)
                keyword = genre_taken
            elif country_taken and not genre_taken:
                filterig = filterig.filter(country = country_taken)
                keyword = country_taken
            elif genre_taken and country_taken:
                if len(filterig.filter(country = country_taken).filter(genre = genre_taken)) == 0:      
                    if r_country < r_genre:
                        filterig = filterig.filter(country = country_taken)
                        keyword = country_taken
                    else:
                        filterig = filterig.filter(genre = genre_taken)
                        keyword = genre_taken
                else:
                    filterig = filterig.filter(country = country_taken).filter(genre = genre_taken)
                    keyword = "%s %s" % (country_taken, genre_taken)
            keyword = "關鍵字: %s | %d筆" % (keyword, len(filterig))
            if text.find('最新'):
                filterig = filterig.order_by('create_at')
            if text.find('推薦'):
                filterig = filterig.order_by('likes')
            api.profileTemplates(filterig)
            api.text_message(keyword)
            api.quickreply_button_message("範例 \"我要看馬來西亞正妹\" \"我要看最新空姐正妹\" \"我要看臺灣模特兒正妹\"", messages['viewig_quickreply'],messages['returnlobby_button'])
            

    def on_enter_uploadprocess(self, sender_id, text):
        api = MessageAPI(sender_id)
        textlist = text.split(' ')
        if len(textlist) >= 4 or len(textlist) == 0:
            api.text_message("格式錯誤請重新再試")
            self.gobackupload(sender_id, text)
        elif textlist[0] == 'payload_like':
            liked_entry = Instagrammer.objects.get(id=textlist[1])
            liked_entry.likes += 1
            liked_entry.save()
            api.text_message("You Liked %s, Now %d Likes"%(textlist[1],liked_entry.likes))
            self.gobackupload(sender_id, text)
        else:
            genre = "無"
            country = "無"
            textlist = text.split(' ')
            if len(textlist) == 3:
                genre = textlist[1]
                country = textlist[2]
            elif len(textlist) == 2:
                genre = textlist[1]
            entry = Instagrammer.objects.filter(id = textlist[0])
            if entry.exists():
                entry = Instagrammer.objects.get(id = textlist[0])
                api.text_message("資料已經在資料庫了，棒棒的，看來妹子很有名哦～")
                entry.country = country
                entry.genre = genre
                entry.save()
            else:
                image_url, bio = getImageUrl(textlist[0])
                Instagrammer.objects.create(
                    id = textlist[0],
                    genre = genre,
                    country = country,
                    content = bio,
                    url = "https://www.instagram.com/%s" % textlist[0],
                    image_url = image_url
                )
            entry = Instagrammer.objects.get(id = textlist[0])
            api.profileTemplatesSingle(entry)
            self.gobackupload(sender_id, text)