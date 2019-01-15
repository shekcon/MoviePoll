from django.contrib import admin

# Register your models here.
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'pub_date')
    list_display_links = ('id', 'question_text')
    list_per_page = 25

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_text', 'question', 'votes')
    list_display_links = ('id', 'choice_text')
    list_filter = ('question',)
    list_per_page = 25

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)