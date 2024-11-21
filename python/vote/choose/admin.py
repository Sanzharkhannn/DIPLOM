from django.contrib import admin
from .models import Option
from .models import VoteOpt


# Register your models here.
admin.site.register(Option)
admin.site.register(VoteOpt)