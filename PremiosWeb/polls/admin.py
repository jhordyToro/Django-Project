#polls/admin.py
from django.contrib import admin
from .models import Choise, Question

# Register your models here.
#Creando un TabularInLine desde el modelo Choise
class ChoiseInline(admin.StackedInline):
    model = Choise
    extra = 3

#Creando un ModelAdmin desde el modelo Question
class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    inlines = [ChoiseInline]
    list_display = ('question_text', 'pub_date', 'time_antique' )
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
