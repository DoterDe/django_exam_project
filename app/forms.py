
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile1
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserProfileForm(UserChangeForm):
    class Meta:
        model = UserProfile1
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'avatar' ]  
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

class Register(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'style': 'width: 300px; margin: 0;'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'style': 'width: 300px; margin: 0;'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'})
    )
    phone_number = forms.CharField(
        max_length=17,
        validators=[UserProfile1.phone_regex],
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона', 'style': 'width: 300px; margin: 0;'})
    )

    class Meta:
        model = UserProfile1
        fields = ['first_name', 'last_name', 'avatar', 'phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        return phone_number

class CodeForm(forms.Form):
    key = forms.IntegerField(
        label='Код подтверждения',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите код',
            'style': 'width: 300px; margin: 0;',
            'required': 'required',
        })
    )

class FormReg(UserCreationForm):
    email = forms.EmailField(       
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email','style' :'width: 300px ;margin: 0;'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username','style' : 'width: 300px ; margin: 0;'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter a strong password','style' : 'width: 300px ; margin: 0;'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password','style' : 'width: 300px ; margin: 0;'})
    )

    class Meta:
        model = UserProfile1
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(FormReg, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = ''

# class FormLogin(AuthenticationForm):
#     username = forms.CharField(
#         label = '',
#         widget=forms.TextInput(attrs={'placeholder': 'Username',
#                                       'style' : 'width: 300px ; margin: 0;'})
#     )
#     password = forms.CharField(
#         label = '',
#         widget=forms.PasswordInput(attrs={'placeholder': 'Password',
#                                       'style' : 'width: 300px ; margin: 0;'})
#     )

class FormLogin(AuthenticationForm):
    username = forms.CharField(label='', max_length=30)
    password = forms.CharField(label='', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя' , 'id': 'id_login_username' })
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль' , 'id': 'id_login_password'})

class UserForm(AuthenticationForm):
    class Meta:
        model = User
        fields =  ['username', 'password' ]


class CreatePostForm(UserCreationForm):
    
    class Meta:
        model = UserProfile1
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar', 'phone_number']