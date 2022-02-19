from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(), 'current_category': current_category}
# 模板标签
# 这段代码定义了一个名为 get_category_list() 的函数，返回结果为分类列表。但是从
# register.inclusion_tag() 装饰器可以看出，这个函数需要 rango/cats.html 模板的支持。创建这个
# 模板，写入下述 HTML 标记