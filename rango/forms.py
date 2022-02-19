from django import forms
from rango.models import Page, Category
from rango.models import User, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Please enter the category name.")
    # widget 小工具
    views= forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)
    # CategoryForm 中包含 slug 字段，但是没有为其指定初始值或默认值，而是隐藏了，并且指明这个
    # 字段不是必须的。这是因为模型在调用 save() 方法保存时会生成这个字段的值。
    
    # 嵌套的类，为表单提供额外信息
    class Meta:
        # 把这个 ModelForm 与一个模型连接起来
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH,help_text="Please enter the title of the page.")
    # url = forms.URLField(max_length=200,help_text="Please enter the URL of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH,help_text="Please enter the URL of the page.")
    # widget=forms.HiddenInput()表示把这个字段藏起来
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    
    
    class Meta:
        # 把这个 ModelForm 与一个模型连接起来
        model = Page
        # 排除'category'
        exclude = ('category',)
    # 想在表单中放哪些字段？
    # 有时不需要全部字段
    # 有些字段接受空值，因此可能无需显示
    # 这里我们想隐藏外键字段
    # 为此，可以排除 category 字段
    # 也可以直接指定想显示的字段（不含 category 字段），如下：
    # fields = ('title', 'url', 'views')
    
    # 重写clean()方法
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
    
    
    
    