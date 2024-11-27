from django.template import loader # type: ignore
from django.http import HttpResponse # type: ignore
from django.shortcuts import render # type: ignore

from django.shortcuts import get_object_or_404, redirect # type: ignore
from django.template.response import TemplateResponse # type: ignore


from django.contrib.auth.decorators import login_required # type: ignore


# Create your views here.


def index(request):
    template = loader.get_template('choose/index.html')
    return HttpResponse(template.render())


