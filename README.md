# 網美IG - Messenger Chat Bot

### 前言：
自己跟一些朋友有這跟別人不一樣的 Messenger Group， 你知道的... 就是會互相分享一些照片或者 Instagram 的 Profile。事實上，要爬 IG 並不是一件很簡單的事情，我們男人也不是 Instagram Explore 隨意幾個美女就可以滿足的，所以我突發奇想，做一個能整合這些網美們的 IG，供大家欣賞。

# 網美IG
## Demo

![](https://i.imgur.com/ZhdmlXr.jpg)
![](https://i.imgur.com/vo9Hdlb.jpg)
![](https://i.imgur.com/NKcQhSe.jpg)
![](https://i.imgur.com/r6s0VyK.jpg)
![](https://i.imgur.com/L4pAk0C.jpg)
![](https://i.imgur.com/rUx3tcb.jpg)

## 功能

- **提供IG大頭照 :**
    不光是IG大頭照好了，所有的IG照片都麼辦法隨意下載，也很厭倦要一張    照片還要ScreenShot 所以只好用一些API的幫助，截取大頭照
- **看正妹 :**
    這個粉專(APP)開來就是來看正妹的，給你 Instagrammer 回去好好追蹤欣賞
- **貢獻 :**
    這個平臺不只是提供欣賞而已哦，我還要使用者上傳，這樣這個平臺就比較多元，從而知道大家都喜歡什麼樣的美女，都在蒐藏些什麼，所以你的貢獻～ 很重要
    
## FSM
![](https://i.imgur.com/A7loJoH.png)
我已分成三個支線作介紹

------------------------------

**lobby 服務大廳**
回覆格式 ： Text, Button
介紹 ： 服務大廳，介紹這個ChatBot大概在做什麼

------------------------------
**instadp 大頭照下載器**
回覆格式 : Text, Button
介紹 ： 介紹Instadp是什麼服務

**instadpinput 得取Instagrammer ID**
回覆方式 : Text, Button, Quick Reply
介紹 ： 在這邊輸入有效的ID name

**printinstadp 顯示大頭照**
回覆方式 ： Attachment(Image)
介紹 ： Bot 會傳那個賬戶的大頭照給你，有別於“看正妹”服務（等下介紹），這個照片是可以點擊後下載在本地端的，而看正妹的是 Template Message

**instadperror 顯示錯誤ID**
回覆方式 : Text
介紹 : 僅傳錯誤訊息給你，將重返 instadpinput

**printdpserver 顯示照片上傳伺服器**
回覆方式 : Text, Generic Template
介紹 : 若選擇上傳剛剛下載的那個賬戶照片，她就會被記錄在Server裏，因爲我覺得既然你要她的大頭照，代表這個Instagrammer有一定的美～

------------------------------

**igviewer 看正妹**
回覆格式 : Text, Button, Quick Reply
介紹 ： 看正妹大廳，提供關鍵字快速回覆，方便搜尋

**viewig 看到正妹**
回覆方式 ： Text, Generic Template， Quick Reply， Buttom
介紹 : 可能搜尋一次不過硬在這個State可以一直搜尋，不要了則返回。如果點擊Like,就會幫妹子集氣哦！！

------------------------------

**iguploader 貢獻IG**
回覆方式 : Text
介紹 : 要求使用者按照格式輸入貢獻資料，這樣漂亮的妹妹才能在看正妹服務被看到

**Uploadprocess 顯示Upload結果**
回覆方式 : Generic Template
介紹 : 把傳好的結果給你看看，如果格式錯誤也會告訴你

------------------------------

## 特別功能

- **平臺特色**
    目的是爲了讓大家能多多分享一下IG,因爲自己也會追蹤XD
    但是一般的 IG 也可以自己看正妹，沒錯，我這個Platform其實也就是幫你找正妹而已，我還是會把正妹還給你(就開鏈接給你自己去追蹤)
    那爲什麼還要這個平臺？本身認爲光靠Instagram的Explore服務是不夠的，它的內容太廣，也不一定都是你喜歡的。而我們通常追蹤一些賬號，不只是它們漂亮而已，往往是一些網路紅人啊，某一個小有名氣的正妹。
    我希望是跟我們貼切的，提供一些關鍵字，或者自己的平臺也可以放Like系統，讓大家看看，大家都喜歡哪一種類型，不然的話，IG 本事很多正妹，但是我確認爲一樣正的他們的追蹤人數並不一樣，所以我得Like系統也是另一種指標。

- **Generic Template**
    顯示正妹的資料 ： BIO , 伺服器分類國家， 伺服器分類類型， 自己系統的Likes
    Default Operation : 點擊直接Redirect去該IG的Profile
    Like Button : 共鳴的Like，正妹有 Like 就會呈現
    ![](https://i.imgur.com/o0Vf6Ht.jpg)

    
- **Postgres Database** **Heroku**
    直接利用Heroku的DB
    我是用 Django 
    我的 Model:
    ```
    class Instagrammer(models.Model):
        # 賬戶 ID
        id = models.TextField(primary_key=True)
        # 網美類型
        genre = models.TextField(default='')
        # 網美國家
        country = models.TextField(default='')
        # 日期
        create_at = models.DateTimeField(auto_now_add=True)
        # 簡單敘述
        content = models.TextField(default="")
        # 賬戶網址
        url = models.URLField(blank=True)
        # 大頭照
        image_url = models.URLField(default="")

        # 人氣
        likes = models.IntegerField(default=0)
        class Meta:
            db_table = "instagrammer"
    ```
    Create Date 可以讓資料可以 Order_By (Django Queryset)
    人氣也可以排序
    
- **小型 Instagram Api**
    說穿了就是去搜 ig 的使用者資料 (publically)
    實現方式 : 
    普通的ig id 應該是 "cabc_123" 之類的
    但是向 `instagram.com/id` 做 Get request可以爬到另一個id
    例如我得臉書叫：張財實，但是爬完資料 我得 id 是：123521000215 (unique)
    後來再用這個id去 
    ```
    url="https://i.instagram.com/api/v1/users/{id}/info/"
    r = requests.get(url.format(userID))
    ```
    request的使用者資料裏就有一個key是使用者的大頭照！！我是這樣抓照片下來的
    
- **IMGUR API**
    因爲處理好的照片沒辦法放Local,其實我也不想，加上之前知道hackmd丟照片自動轉成imgur的照片來serve。
    所以我想要讓收好的照片以Url的方式呈現（方便DB管理，直接給FB用）
    `n = requests.post("https://api.imgur.com/3/image", headers={"Authorization": "Bearer %s" % IMGUR_ACESS_TOKEN}, data={"image":r.content})`
    照片：
    
- **Multiple User**
    知道一個user一個machine的原理 其實這樣實現multiple user 就可以了
    想要有多個人跟你的page聯繫，就要把朋友加入test user role
 ```
    if sender_id not in machine:
        machine[sender_id] = TocMachine(
            states=machineSet["states"],
            transitions=machineSet["transitions"],
            initial=machineSet["initial"],         
            auto_transitions=machineSet["auto_transitions"],
        )
```

- **Deploy**
    Deployed On Heroku
    https://instagrammer-mes.herokuapp.com/
    ![](https://i.imgur.com/wwEl6Pb.png)
    
- **RESTFUL API**
    因爲django framwork很完善所以我就把API也寫一寫了
    單筆更改資料就很好用了 支援 GET POST PUT DELETE
    ![](https://i.imgur.com/6SGAIyv.png)

