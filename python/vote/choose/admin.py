from django.contrib import admin
from .models import Content, Vote, ContentOptionVote, ContentOption, UserRSAKeys   # Импортируем модели, а не формы



class ContentOptionInline(admin.TabularInline):
    model = ContentOption
    extra = 0


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__username')
    list_filter = ('created_at',)
    inlines = [ContentOptionInline]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'vote_type', 'content', 'target_user', 'created_at')
    search_fields = ('voter__username', 'content__title', 'target_user__username')
    list_filter = ('vote_type', 'created_at')


@admin.register(ContentOption)
class ContentOptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'content', 'get_votes_count')
    search_fields = ('option_text', 'content__title')

    def get_votes_count(self, obj):
        return obj.votes.count()
    get_votes_count.short_description = 'Кол-во голосов'


@admin.register(ContentOptionVote)
class ContentOptionVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'voted_at')
    search_fields = ('user__username', 'option__option_text')
    list_filter = ('option__content',)

@admin.register(UserRSAKeys)
class UserRSAKeysAdmin(admin.ModelAdmin):
    list_display = ('user', 'public_key')
    search_fields = ('user__username',)


# Регистрируем модели в админке
# admin.site.register(Content)
# admin.site.register(Vote)
# @admin.register(UserRSAKeys)
# class UserRSAKeysAdmin(admin.ModelAdmin):
#     list_display = ('user',)
