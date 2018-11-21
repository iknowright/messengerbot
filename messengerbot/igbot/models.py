from django.db import models

# Create your models here.

class Instagrammer(models.Model):
    # 賬戶 ID
    id = models.TextField(primary_key=True)
    # 網美類型
    genre = models.TextField(default='無')
    # 網美國家
    create_at = models.DateTimeField(auto_now_add=True)
    # 簡單敘述
    content = models.TextField(default="")
    # Thunbnail

    # 賬戶網址
    url = models.URLField(blank=True)

    class Meta:
        db_table = "instagrammer"