# ake sure you have imported your project’s settings by importing django and setting the environment variable
# DJANGO_SETTINGS_MODULE to be your project’s setting file
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

# You then call django.setup() to import your Django project’s settings.
import django
django.setup()

# 如果没有上面的import和setup()的话，这里导入model就会出错！
from rango.models import Category, Page

# 时间模块
from django.utils import timezone

def populate():
    # First, we will create lists of dictionaries containing the pages we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    # 首先，我们将创建包含我们要添加到每个类别中的页面的字典列表。
    # 然后我们将为我们的类别创建一个字典的字典。
    # 这可能看起来有点混乱，但它允许我们迭代
    # 通过每个数据结构，并将数据添加到我们的模型中。
    python_pages = [
        {'title': 'Official Python Tutorial', 'url':'http://docs.python.org/3/tutorial/', 'views':15},
        {'title': 'How to Think like a Computer Scientist', 'url':'http://www.greenteapress.com/thinkpython/', 'views':10},
        {'title': 'Learn Python in 10 Minutes', 'url':'http://www.korokithakis.net/tutorials/python/', 'views':8} ]


    django_pages = [
        {'title':'Official Django Tutorial', 'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views':6},
        {'title':'Django Rocks', 'url':'http://www.djangorocks.com/', 'views':2},
        {'title':'How to Tango with Django', 'url':'http://www.tangowithdjango.com/', 'views':20} ]

    other_pages = [
        {'title':'Bottle', 'url':'http://bottlepy.org/docs/dev/', 'views':16},
        {'title':'Flask', 'url':'http://flask.pocoo.org', 'views':11} ]



    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
        'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
        'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.

    # 下面的代码会浏览猫的字典，然后添加每个类别。
    # 然后添加该类别的所有相关页面。
    # cat 是key， cat_data 是value
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])


# Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views):
    # object相当于是一个map(key,value)
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    # p.pub_date=timezone.now()
    p.save()

'''  
# 多行注释
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    if(c.name == 'Python'):
        c.views = 128
        c.likes = 64
    if(c.name == 'Django'):
        c.views = 64
        c.likes = 32
    if(c.name == 'Other Frameworks'):
        c.views = 32
        c.likes = 16
    c.save()
    return c
'''

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

#start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()




