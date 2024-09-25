
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CreatePostForm , UserForm , FormLogin, FormReg , CodeForm,Register
from .models import UserProfile1,Product
from django.views.generic.edit import CreateView, DeleteView
from .serializers import ProductSerializers
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate
import random
from django.conf import settings




def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

def register_and_login_view(request):
    signup_form = FormReg()
    login_form = FormLogin()

    if request.method == 'POST':
        if 'signup_submit' in request.POST:
            signup_form = FormReg(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_active = False 
                user.code = generate_code()  
                user.save()  

                code = user.code  
                message = f'Ваш код подтверждения: {code}'
                send_mail(
                    'Код подтверждения',
                    message,
                    settings.EMAIL_HOST_USER,
                    [signup_form.cleaned_data['email']],
                    fail_silently=False
                )

                return redirect('enter_confirmation_code', user_id=user.id) 

        elif 'login_submit' in request.POST:
            login_form = FormLogin(request=request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли в систему.')
                    return redirect('home')
                else:
                    messages.error(request, "Аутентификация не удалась: неверное имя пользователя или пароль.")
            else:
                messages.error(request, "Форма входа недействительна. Пожалуйста, исправьте ошибки ниже.")

    return render(request, 'authenticate/register_and_login.html', context={'signup_form': signup_form, 'login_form': login_form})

def enter_confirmation_code(request, user_id):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code_use = form.cleaned_data.get("key")
            try:
                user = UserProfile1.objects.get(id=user_id)
                if user.code == code_use:
                    user.is_active = True 
                    user.code = generate_code() 
                    user.save()
                    login(request, user)
                    messages.success(request, 'Ваш аккаунт успешно подтверждён.')
                    return redirect('register', user_id=user.id)
                else:
                    form.add_error(None, 'Неверный код подтверждения.')
            except UserProfile1.DoesNotExist:
                form.add_error(None, 'Пользователь не найден.')
    else:
        form = CodeForm()

    return render(request, 'authenticate/enter_code.html', {'form': form})

def register(request, user_id):
    user = UserProfile1.objects.get(id=user_id) 
    if request.method == 'POST':
        form = Register(request.POST, instance=user)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация завершена успешно.')
            return redirect('home')
        else:
            messages.error(request, "Ошибка при регистрации. Пожалуйста, исправьте ошибки ниже.")
    else:
        form = Register(instance=user)

    return render(request, 'authenticate/register.html', {'form': form}) 


@login_required
def profile_view(request):
    user_profile = UserProfile1.objects.get(user=request.user)
    return render(request, 'profile.html', {'userprofile1': user_profile})



@permission_classes((IsAuthenticated,))
class APIProductViewSet(ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializers


class APIREADProductViewSet(ReadOnlyModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = (IsAuthenticated,)

# class APIProduct(generics.ListAPIView):
#     queryset =  Product.objects.all()
#     serializer_class = ProductSerializers

# class APIProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset =  Product.objects.all()
#     serializer_class = ProductSerializers



# @api_view(['GET', 'POST'])
# def api_product (request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializers(products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializers(data=request.data) 
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE']) 
# def api_product_id(request, pk): 
#     rubric = Product.objects.get(pk=pk) 
#     if request.method == 'GET': 
#         serializer = ProductSerializers(rubric) 
#         return Response(serializer.data) 
#     elif request.method == 'PUT' or request.method == "PATCH": 
#         serializer = ProductSerializers(rubric, data=request.data, partial = True) 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
#     elif request.method == 'DELETE': 
#         rubric.delete() 
#         return Response ('Success delete',status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def api_rubrics(request) : 
#     if request.method == 'GET':
#         rubrics = Product.objects.all() 
#         serializer = RubricSerializer (rubrics, any-Irel retumn Response (serializer.data) elif request.method = 'POST': serializer = RubricSerializer (data=request .data) if serializer.is valid(): serializer.save () return Response (serializer.data, status=status.HTTP 201 CBATED return Response (serializer.errors, status-status.HITP 400 BAD REQUEST]

def home(request):
    posts=UserProfile1.objects.all()
    if request.method == 'POST':
        api_id = request.POST['id_product']
        return redirect(f'api_id/{api_id}')

    return render(request, 'home.html', context= {'posts':posts } )

# @api_view(['GET'])
# def api_product(request):
#     if request.method == 'GET':
#         product = Product.objects.all()
#         serializer = ProductSerializers(product, many = True)
#         return Response(serializer.data)
# @api_view(['GET'])
# def api_product_id(request, pk):
#     if  request.method == 'GET':
#         product = Product.objects.get(pk=pk)
#         serializer = ProductSerializers(product)
#         return Response(serializer.data)






def email_massage(request):
    user = UserProfile1.objects.get(id=1)
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        [f"{user.email}"],
        fail_silently=False,
    )
    return HttpResponseRedirect("/")

class CreatePost(CreateView):
    model = UserProfile1    
    success_url = reverse_lazy('login')
    template_name = 'create.html'
    form_class = CreatePostForm

class DeletePost(DeleteView):
    model = UserProfile1   
    success_url = reverse_lazy('home')
    template_name = 'delete.html'

@login_required
def logout_student(request):
    logout(request)
    return render(request, 'home.html')