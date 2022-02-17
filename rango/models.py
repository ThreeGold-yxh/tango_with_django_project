# models.py 模块的顶部应该有 from django.db import models。如果没有，自己动手加上。
import datetime
import imp
from unicodedata import category
import django
from django.db import models
from django.utils import timezone
# 导入 slugify() 函数
from django.template.defaultfilters import slugify

# 注意 model类 都是数据库相关
# Create your models here.
# 这个model类表示 分类，它要继承django.db.models.Model，也就是括号中的内容
class Category(models.Model):
    NAME_MAX_LENGTH = 128
    # name字段是独一无二的，而且长度为128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    # 更新 Category 模型，加上 views 和 likes 字段，二者的默认值均是零。
    # views 是查看次数，likes是点赞次数
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    # 注意，只要分类名称变了，别名就随之改变。
    # slug = models.SlugField()
    
    # 解决方法一，更新模型，把 slug 字段设为允许空值
    slug = models.SlugField(blank=True)
    
    # 第二个问题也不难解决，只需把 slug 字段设为唯一的。为 slug 字段添加约束
    # slug = models.SlugField(unique=True)
    
    # save方法
    # 通过迁移工具能把 slug 字段添加到数据库中，而且可以为该字段指定默认值。
    # 可是，每个分类的别名应该是不同的。因此，我们将先执行迁移，然后重新运行填充脚本。之所
    # 以这么做，是因为填充脚本会在分类上调用 save() 方法，从而触发上面实现的 save() 方法，更新各分类的别名。
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    # 特殊的复数形式
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

# 这个分类表示 网页
class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', default = timezone.now)
    # 判断是不是近期发布的，一天内
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # __str__()
    def __str__(self):  
        return self.title

