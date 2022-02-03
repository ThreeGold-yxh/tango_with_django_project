from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse("Rango says hey there partner!")
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # 构建一个字典，传递给模板引擎作为其上下文。
    # 注意键boldmessage与模板中的{{ boldmessage }}相匹配!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake'}

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

