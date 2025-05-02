

from django.contrib import admin
from .models import Content, Vote, ContentOption, UserRSAKeys, EncryptedVote  # Импортируем только нужные модели


class ContentOptionInline(admin.TabularInline):
    model = ContentOption
    extra = 0


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'start_date', 'end_date')
    list_filter = ('created_at', 'start_date', 'end_date')
    search_fields = ('title', 'body', 'user__username')
    readonly_fields = ('public_key', 'private_key_encrypted')
    inlines = [ContentOptionInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'body', 'start_date', 'end_date')
        }),
        ('Ключи шифрования', {
            'classes': ('collapse',),
            'fields': ('public_key', 'private_key_encrypted'),
            'description': 'PEM-представление ключей (public, private зашифрованный)'
        }),
    )


@admin.register(EncryptedVote)
class EncryptedVoteAdmin(admin.ModelAdmin):
    list_display = ('content', 'voted_at')
    list_filter = ('voted_at',)
    search_fields = ('content__title',)
    readonly_fields = ('encrypted_choice',)


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


@admin.register(UserRSAKeys)
class UserRSAKeysAdmin(admin.ModelAdmin):
    list_display = ('user', 'public_key')
    search_fields = ('user__username',)






# from django.contrib import admin
# from .models import Content, Vote, ContentOption, UserRSAKeys,EncryptedVote   # Импортируем модели, а не формы



# class ContentOptionInline(admin.TabularInline):
#     model = ContentOption
#     extra = 0


# # @admin.register(Content)
# # class ContentAdmin(admin.ModelAdmin):
# #     list_display = ('title', 'user', 'created_at')
# #     search_fields = ('title', 'user__username')
# #     list_filter = ('created_at',)
# #     inlines = [ContentOptionInline]


# @admin.register(Content)
# class ContentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'user', 'created_at', 'start_date', 'end_date')
#     list_filter = ('created_at', 'start_date', 'end_date')
#     search_fields = ('title', 'body', 'user__username')
#     readonly_fields = ('public_key', 'private_key_encrypted')
#     fieldsets = (
#         (None, {
#             'fields': ('user', 'title', 'body', 'start_date', 'end_date')
#         }),
#         ('Ключи шифрования', {
#             'classes': ('collapse',),
#             'fields': ('public_key', 'private_key_encrypted'),
#             'description': 'PEM-представление ключей (public, private зашифрованный)'
#         }),
#     )


# # @admin.register(ContentOptionVote)
# # class ContentOptionVoteAdmin(admin.ModelAdmin):
# #     list_display = ('user', 'option', 'voted_at')
# #     list_filter = ('voted_at',)
# #     search_fields = ('user__username', 'option__option_text')


# @admin.register(EncryptedVote)
# class EncryptedVoteAdmin(admin.ModelAdmin):
#     list_display = ('content', 'voted_at')
#     list_filter = ('voted_at',)
#     search_fields = ('content__title',)
#     readonly_fields = ('encrypted_choice',)


# @admin.register(Vote)
# class VoteAdmin(admin.ModelAdmin):
#     list_display = ('voter', 'vote_type', 'content', 'target_user', 'created_at')
#     search_fields = ('voter__username', 'content__title', 'target_user__username')
#     list_filter = ('vote_type', 'created_at')


# @admin.register(ContentOption)
# class ContentOptionAdmin(admin.ModelAdmin):
#     list_display = ('option_text', 'content', 'get_votes_count')
#     search_fields = ('option_text', 'content__title')

#     def get_votes_count(self, obj):
#         return obj.votes.count()
#     get_votes_count.short_description = 'Кол-во голосов'


# # @admin.register(ContentOptionVote)
# # class ContentOptionVoteAdmin(admin.ModelAdmin):
# #     list_display = ('user', 'option', 'voted_at')
# #     search_fields = ('user__username', 'option__option_text')
# #     list_filter = ('option__content',)

# @admin.register(UserRSAKeys)
# class UserRSAKeysAdmin(admin.ModelAdmin):
#     list_display = ('user', 'public_key')
#     search_fields = ('user__username',)


# # Регистрируем модели в админке
# # admin.site.register(Content)
# # admin.site.register(Vote)
# # @admin.register(UserRSAKeys)
# # class UserRSAKeysAdmin(admin.ModelAdmin):
# #     list_display = ('user',)
