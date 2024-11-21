from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Option
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from .forms import PollForm 
from .models import Option

# Create your views here.


def create_poll(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            
            # Добавляем опции
            options = request.POST.getlist('options[]')
            for option_text in options:
                Option.objects.create(poll=poll, text=option_text)
            
            return redirect('poll_detail', poll_id=poll.id)
    else:
        poll_form = PollForm()

    return render(request, 'choose/create_poll.html', {'poll_form': poll_form})



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
        VoteOpt.objects.create(option=option, voter=request.user)
        option.total_votes += 1
        option.save()
        return redirect('choose:option_list')  # Перенаправление на список вариантов

    return render(request, 'choose/vote.html', {'option': option})
    
'''