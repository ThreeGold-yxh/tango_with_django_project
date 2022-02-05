
# Register your models here.
from django.contrib import admin
from rango.models import Category, Page

# admin.site.register(Category)
# admin.site.register(Page)

class PageAdmin(admin.ModelAdmin):
    # fields = ['public_date', 'question_text']
    # 默认情况下，Django 显示每个对象的 str() 返回的值。但有时如果我们能够显示单个字段，
    # 它会更有帮助。为此，使用 list_display 后台选项，它是一个包含要显示的字段名的元组，
    # 在更改列表页中以列的形式展示这个对象：
    list_display = ('title', 'category', 'url')


admin.site.register(Category)
admin.site.register(Page, PageAdmin)

