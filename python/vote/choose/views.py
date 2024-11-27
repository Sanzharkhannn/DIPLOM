from django.template import loader # type: ignore
from django.http import HttpResponse # type: ignore
from django.shortcuts import render # type: ignore

from django.shortcuts import get_object_or_404, redirect # type: ignore
from django.template.response import TemplateResponse # type: ignore
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout # type: ignore

from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Импортируем вашу форму для регистрации


# Create your views here.


def index(request):
    template = loader.get_template('choose/index.html')
    return HttpResponse(template.render())


# Функция регистрации
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Создаём пользователя
            auth_login(request, user)  # Автоматически логиним после регистрации
            return redirect('index')  # Перенаправляем на главную страницу
    else:
        form = CustomUserCreationForm()  # Пустая форма для отображения
    return render(request, 'choose/register.html', {'form': form})

# Функция логина
def user_login(request):  # Переименована функция для предотвращения рекурсии
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Логиним пользователя
            return redirect('index')  # Перенаправляем на главную страницу
        else:
            return render(request, 'choose/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'choose/login.html')  # Отображаем форму логина

# Функция логаута
def user_logout(request):  # Переименована для предотвращения рекурсии
    auth_logout(request)  # Выход из системы
    return redirect('login')  # Перенаправляем на страницу логина