from unicodedata import name
from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    # 就是在URL为....../rango/时，/rango被tango_with_django_project中的urls.py处理了，分发到我们rango这个app下的urls.py中
    # 然后如果rango后面什么都没有了，那么对应''，我们rango里面的映射，把它映射到views.py文件下的index方法，返回一个搞静态的页面
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    ]


