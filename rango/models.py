# models.py 模块的顶部应该有 from django.db import models。如果没有，自己动手加上。
from unicodedata import category
from django.db import models

# 注意 model类 都是数据库相关
# Create your models here.
# 这个model类表示 分类，它要继承django.db.models.Model，也就是括号中的内容
class Category(models.Model):
    # name字段是独一无二的，而且长度为128
    name = models.CharField(max_length=128, unique=True)
    def _str_(self):
        return self.name

# 这个分类表示 网页
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

