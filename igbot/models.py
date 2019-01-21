from django.db import models

# Create your models here.

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

class Token(models.Model):
    short_lived_user_access_token = models.TextField(default="")
    long_lived_user_access_token = models.TextField(default="")
    page_access_token = models.TextField(default="")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Tokens"