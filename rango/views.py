from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rango.models import Category
# 首先导入 Page 模型，即把下述导入语句添加到文件顶部：
from rango.models import Page

# 在文件顶部添加这个导入语句
from rango.forms import CategoryForm

from rango.forms import PageForm

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

def add_category(request):
    form = CategoryForm()
    
    # 是 HTTP POST 请求吗？
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        # 表单数据有效吗？
        if form.is_valid():
            
            # 把新分类存入数据库
            '''
            确认分类成功添加的另一种方法是修改 rango/views.py 文件中的 add_category() 函数,把
            form.save(commit=True) 改成 cat = form.save(commit=True),为通过表单创建的分类对象
            提供一个引用,这样便可以在控制台中打印分类,例如 print(cat, cat.slug)。
            '''
            cat = form.save(commit=True)
            
            # 保存新分类后可以显示一个确认消息
            # 不过既然最受欢迎的分类在首页
            # 那就把用户带到首页吧
            # return index(request)
        
            # 用重定向
            return redirect('/rango/')
        else:
            
            # 表单数据有错误
            # 直接在终端里打印出来
            print(form.errors)
            
    # 处理有效数据和无效数据之后
    # 渲染表单，并显示可能出现的错误消息
    return render(request,'rango/add_category.html',{'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')    
    
    form = PageForm()
    # 是HTTP POST 请求吗？
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        # 表单数据有效吗？
        if form.is_valid():
            if category:
                # 先拿到form对象
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                # form.save(commit=True)
                page.save()
                # probably better to use a redirect here.
            # 虽然这种写法比较好, 但无法通过测试
            # return show_category(request, category_name_slug)
            
            # 用重定向
            return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    
    
    # 处理有效数据和无效数据之后
    # 渲染表单，并显示可能出现的错误消息
    return render(request, 'rango/add_page.html', context_dict)