from django.shortcuts import render
from .models import Option
from .models import Vote
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def chooses(request):
    template = loader.get_template('choose/index.html')
    return HttpResponse(template.render())

'''
def option_list(request):
    optionLists = Option.objects.all()
    return render(request,
                  'choose/option/list.html',
                  {'options' : optionLists})


def vote(request, option_id):
    option = get_object_or_404(Option, id=option_id)
    # Логика для обработки голосования
    if request.method == 'POST':
        # Создание нового голосования
        Vote.objects.create(option=option, voter=request.user)
        option.total_votes += 1
        option.save()
        return redirect('choose:option_list')  # Перенаправление на список вариантов

    return render(request, 'choose/vote.html', {'option': option})
    
    '''