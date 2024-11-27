from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse


from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    template = loader.get_template('choose/index.html')
    return HttpResponse(template.render())


def option_list(request):
    optionLists = Option.objects.all()
    option_dict = {
        'options': optionLists
    }
    return render(request,
                  'choose/option/list.html',
                    option_dict)

def create_option(request):
    if request.method == 'POST':
        # Получение данных из POST-запроса
        text = request.POST.get('text')  # Текст

        if text:  # Проверка на заполнение полей
            # Создание нового объекта Option
            Option.objects.create(text=text)
            return redirect('option_list')  # Перенаправление на список вариантов
        else:
            return HttpResponse("Не все поля заполнены!", status=400)

    # Если запрос GET, отобразить форму
    return render(request, 'choose/create_option.html')


