from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
# 首先导入 Page 模型，即把下述导入语句添加到文件顶部：
from rango.models import Page

# Create your views here.
def index(request):
    # return HttpResponse("Rango says hey there partner!")
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # 构建一个字典，传递给模板引擎作为其上下文。
    # 注意键boldmessage与模板中的{{ boldmessage }}相匹配!
    # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    bold_message = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    # 查询数据库，获取目前存储的所有分类
    # 按点赞次数倒序排列分类
    # 获取前 5 个分类（如果分类数少于 5 个，那就获取全部）
    # 把分类列表放入 context_dict 字典
    # 稍后传给模板引擎
    category_list =Category.objects.order_by('-likes')[:5]
    
    # 拿到浏览量前五的网站，倒序（由大到小）
    page_list = Page.objects.order_by('-views')[:5]    
    context_dict = {'categories': category_list, 'boldmessage': bold_message, 'pages': page_list}
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # 返回一个渲染好的响应，发送给客户端。
    # 我们利用快捷键函数来使我们的生活更轻松。
    # 注意，第一个参数是我们希望使用的模板。
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # return HttpResponse("Rango says here is the about page!")
    return render(request, 'rango/about.html')

# 然后定义视图 show_category()
def show_category(request, category_name_slug):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}
    
    try:
        # 能通过传入的分类别名找到对应的分类吗？
        # 如果找不到，.get() 方法抛出 DoesNotExist 异常
        # 因此 .get() 方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)
        
        # 检索关联的所有网页
        # 注意，filter() 返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)
        
        # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['pages'] = pages
        # 也把从数据库中获取的 category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None
    #debug: 我这里之前缩进去了    
    # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)
        
'''
这个视图的基本步骤与 index() 视图一样。首先定义上下文字典,然后尝试从模型中提取数据,
并把相关数据添加到上下文字典中。我们通过传给 show_category() 视图函数的
category_name_slug 参数确认要查看的是哪个分类。如果通过别名找到了分类,获取与之关联的
网页,并将其添加到上下文字典 context_dict 中。
'''

