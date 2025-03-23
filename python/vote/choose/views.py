from django.template import loader  # type: ignore
from django.http import HttpResponse, JsonResponse  # type: ignore
from django.shortcuts import render, redirect, get_object_or_404  # type: ignore

from .forms import CustomUserCreationForm, CreateContentForVote
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from .models import Content, Vote,  ContentOption, ContentOptionVote
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
from django.contrib import messages
from .models import Content
# Create your views here.



def index(request):
    return render(request, "choose/index.html")

# Функция регистрации
def user_register(request):
    if request.user.is_authenticated:
        messages.info(request, "Вы уже вошли в систему.")
        return redirect('choose:user-page')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Создаём пользователя
            # Автоматически логиним после регистрации
            auth_login(request, user)
            # Перенаправляем на главную страницу
            return redirect("choose:index")
    else:
        form = CustomUserCreationForm()  # Пустая форма для отображения
    return render(request, "choose/register.html", {"form": form})


# Функция логина


def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, "Вы уже вошли в систему.")
        return redirect('choose:user-page')  # Укажи правильное имя главной страницы

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("choose:logined-page")  # Укажи правильный URL namespace
        else:
            messages.error(request, "Неверный логин или пароль")
            return render(request, "choose/login.html")

    return render(request, "choose/login.html")

@login_required
def logined_page(request):
    return render(request, "choose/logined-page.html")


# Функция логаута


def user_logout(request):  # Переименована для предотвращения рекурсии
    auth_logout(request)  # Выход из системы
    return redirect("choose:user-login")  # Перенаправляем на страницу логина


def vote_page(request):
    return render(request, "choose/vote.html")


 # Убедитесь, что пользователь авторизован
def create_content(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get("title")  # Получаем данные из формы
            body = request.POST.get("body")  # Добавляем поле body

            # Создаем новый объект Content
            Content.objects.create(user=request.user, title=title, body=body)

            # Перенаправляем на страницу успеха или обратно на голосование
            return redirect("choose:vote-success")  # Укажите реальный URL

        # Возвращаем форму для создания контента
        return render(request, "choose/vote.html")
    else:
        return redirect("choose:user-register") 


def vote_success(request):
    return render(
        request,
        "choose/vote_success.html",
        {"message": "Content created successfully!"},
    )


matplotlib.use('Agg')


@login_required
def show_votes(request):
    if request.method == "POST":
        content_id = request.POST.get("content_id")
        vote_type = request.POST.get("vote_type")

        # Получаем объект контента
        content = get_object_or_404(Content, id=content_id)

        # Проверяем, голосовал ли пользователь ранее за этот контент
        existing_vote = Vote.objects.filter(
            voter=request.user, content=content).first()
        if existing_vote:
            # Если пользователь уже голосовал, обновляем голос
            existing_vote.vote_type = vote_type
            existing_vote.save()
        else:
            # Если голос первый, создаём новый
            Vote.objects.create(
                voter=request.user, content=content, vote_type=vote_type
            )

        # Возвращаем JSON-ответ, если голосование происходит через AJAX
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Vote registered!"})

        # Перенаправляем на страницу голосования
        return redirect("choose:vote-page")

    # Считаем голоса для каждого контента и добавляем проценты как атрибуты
    contents = Content.objects.all()

    for content in contents:
        votes = Vote.objects.filter(content=content)
        up_count = votes.filter(vote_type="up").count()
        down_count = votes.filter(vote_type="down").count()
        total_votes = up_count + down_count

        content.up_percent = (100 * up_count) / \
            total_votes if total_votes > 0 else 0
        content.down_percent = (100 * down_count) / \
            total_votes if total_votes > 0 else 0
        content.total_votes = total_votes

        # Построение диаграммы
        # if total_votes > 0:
        #     labels = ['Up Votes', 'Down Votes']
        #     sizes = [content.up_percent, content.down_percent]
        #     colors = ['#4CAF50', '#F44336']

        #     fig, ax = plt.subplots()
        # ax.pie(sizes, labels=labels, colors=colors,
        #        autopct='%1.1f%%', startangle=90)
        # # Equal aspect ratio ensures that pie is drawn as a circle.
        # ax.axis('equal')
        # plt.title(f"{content.title} - {total_votes} Votes")

        # # Сохранение диаграммы в буфер
        # buf = io.BytesIO()
        # plt.savefig(buf, format='png')
        # buf.seek(0)
        # image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        # buf.close()
        # plt.close(fig)

        # # Сохраняем диаграмму как атрибут объекта
        # content.chart_image = f"data:image/png;base64,{image_base64}"

        if total_votes > 0:
            labels = ['Up Votes', 'Down Votes']
            sizes = [content.up_percent, content.down_percent]
            colors = ['#4CAF50', '#F44336']

            fig, ax = plt.subplots()
            ax.bar(labels, sizes, color=colors, width=0.6)

    # Добавляем подписи процентов над столбцами
            for i, v in enumerate(sizes):
                ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=10)

    # Устанавливаем заголовок и подписи осей
            ax.set_title(
                f"{content.title} - {total_votes} Votes", fontsize=14)
            ax.set_xlabel("Vote Type", fontsize=12)
            ax.set_ylabel("Percentage(%)", fontsize=12)

            # Устанавливаем диапазон для оси Y
            ax.set_ylim(0, 100)

            # Сохранение диаграммы в буфер
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            plt.close(fig)

            content.chart_image = f"data:image/png;base64,{image_base64}"
        else:
            content.chart_image = None

    return render(request, "choose/show-votes.html", {"contents": contents})

# @login_required
# def show_votes(request):
#     if request.method == "POST":
#         content_id = request.POST.get("content_id")
#         vote_type = request.POST.get("vote_type")

#         # Получаем объект контента
#         content = get_object_or_404(Content, id=content_id)

#         # Проверяем, голосовал ли пользователь ранее за этот контент
#         existing_vote = Vote.objects.filter(voter=request.user, content=content).first()
#         if existing_vote:
#             # Если пользователь уже голосовал, обновляем голос
#             existing_vote.vote_type = vote_type
#             existing_vote.save()
#         else:
#             # Если голос первый, создаём новый
#             Vote.objects.create(
#                 voter=request.user, content=content, vote_type=vote_type
#             )

#         # Возвращаем JSON-ответ, если голосование происходит через AJAX
#         if request.headers.get("x-requested-with") == "XMLHttpRequest":
#             return JsonResponse({"success": True, "message": "Vote registered!"})

#         # Перенаправляем на страницу голосования
#         return redirect("choose:vote-page")

#     # Считаем голоса для каждого контента и добавляем проценты как атрибуты
#     contents = Content.objects.all()

#     for content in contents:
#         votes = Vote.objects.filter(content=content)
#         up_count = votes.filter(vote_type="up").count()
#         down_count = votes.filter(vote_type="down").count()
#         total_votes = up_count + down_count

#         # Добавляем динамические атрибуты к каждому объекту content
#         content.up_percent = (100 * up_count) / total_votes if total_votes > 0 else 0
#         content.down_percent = (
#             (100 * down_count) / total_votes if total_votes > 0 else 0
#         )
#         content.total_votes = total_votes

#     # Передаём данные в шаблон
#     return render(request, "choose/show-votes.html", {"contents": contents})


def userPage(request):
    return render(request, "choose/userWeb.html")



def worldPage(request):
    return render(request, "choose/world.html")

def create_club_vote(request):
    return render(request, 'choose/create_club_vote.html')

def create_player_vote(request):
    return render(request, 'choose/create_player_vote.html')

def create_movie_vote(request):
    return render(request, 'choose/create_movie_vote.html')

def create_actor_vote(request):
    return render(request, 'choose/create_actor_vote.html')

def create_profession_vote(request):
    return render(request, 'choose/create_profession_vote.html')

def create_famous_vote(request):
    return render(request, 'choose/create_famous_vote.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Content, ContentOption
from django.utils import timezone


@login_required
def create_poll(request):
    if request.method == 'POST':
        vote_title = request.POST.get('vote_title')
        vote_description = request.POST.get('vote_description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        options = request.POST.getlist('vote_options')  # Получаем список всех вариантов
        
        # Создаём запись Content
        content = Content.objects.create(
            user=request.user,
            title=vote_title,
            body=vote_description,
            start_date=start_date,
            end_date=end_date,
            created_at=timezone.now()
        )
        
        # Сохраняем варианты
        for option in options:
            if option.strip():
                ContentOption.objects.create(content=content, option_text=option.strip())
        
        return redirect('choose:vote-list')  # Перенаправляем на страницу списка голосований
    
    return render(request, 'choose/create_poll.html')


def vote_list(request):
    polls = Content.objects.all().order_by('-created_at')
    return render(request, "choose/vote_list.html", {"polls": polls})


# @login_required
# def poll_detail(request, poll_id):
#     poll = get_object_or_404(Content, id=poll_id)
#     if request.method == 'POST':
#         option_id = request.POST.get('option')
#         if option_id:
#             option = get_object_or_404(ContentOption, id=option_id)
#             # Проверяем, голосовал ли уже пользователь
#             existing_vote = ContentOptionVote.objects.filter(user=request.user, option__content=poll).first()
#             if not existing_vote:
#                 ContentOptionVote.objects.create(user=request.user, option=option)
#             return redirect('choose:polls_list')  # или куда-то ещё
#     return render(request, 'choose/poll_detail.html', {'poll': poll})


@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Content, id=poll_id)
    options = ContentOption.objects.filter(content=poll)
    
    if request.method == 'POST':
        selected_option_id = request.POST.get('option')
        if selected_option_id:
            selected_option = ContentOption.objects.get(id=selected_option_id)

            # Проверяем, голосовал ли пользователь ранее
            existing_vote = ContentOptionVote.objects.filter(user=request.user, option__content_id=poll_id).first()
            if existing_vote:
                # Изменяем существующий голос
                existing_vote.option = selected_option
                existing_vote.save()
                messages.success(request, "Ваш голос был обновлен!")
            else:
                # Если не голосовал ранее — создаём новый голос
                ContentOptionVote.objects.create(user=request.user, option=selected_option)
                messages.success(request, "Спасибо за ваш голос!")

            return redirect('choose:poll_detail', poll_id=poll_id)
        else:
            messages.error(request, "Вы не выбрали вариант ответа.")

    return render(request, 'choose/poll_detail.html', {'poll': poll, 'options': options})


def polls_list(request):
    polls = Content.objects.all()
    return render(request, 'choose/polls_list.html', {'polls': polls})