# models.py 模块的顶部应该有 from django.db import models。如果没有，自己动手加上。
import datetime
from unicodedata import category
import django
from django.db import models
from django.utils import timezone

# 注意 model类 都是数据库相关
# Create your models here.
# 这个model类表示 分类，它要继承django.db.models.Model，也就是括号中的内容
class Category(models.Model):
    # name字段是独一无二的，而且长度为128
    name = models.CharField(max_length=128, unique=True)
    # 更新 Category 模型，加上 views 和 likes 字段，二者的默认值均是零。
    # views 是查看次数，likes是点赞次数
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    # 特殊的复数形式
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

# 这个分类表示 网页
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', default = timezone.now)
    # 判断是不是近期发布的，一天内
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # __str__()
    def __str__(self):  
        return self.title

