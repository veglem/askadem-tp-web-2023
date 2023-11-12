from django.contrib import admin
from ask_me import models

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Tag)
admin.site.register(models.QuestionLikes)
admin.site.register(models.AnswerLikes)