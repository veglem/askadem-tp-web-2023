import pgtrigger
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from pgtrigger import *


# Create your models here.

class ProfileManager(models.Manager):
    def get_top_users(self):
        return self.order_by('-likes')[:5]

    def get_user_by_username(self, username):
        try:
            user = self.objects.get(user__username=username)
        except ObjectDoesNotExist:
            user = None

        return user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    likes = models.IntegerField(default=0)

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'


class TagManager(models.Manager):
    def get_question_tags(self, question):
        return self.filter(questions=question)

    def get_top_tags(self):
        return self.annotate(cnt=Count('questions')).order_by('-cnt')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=15)

    objects = TagManager()

    def __str__(self):
        return f"{self.name}"


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-creation_date')

    def get_hot(self):
        return self.order_by('-likes', '-creation_date')

    def get_questions_with_tag(self, tag):
        return self.filter(tags=tag).order_by('-likes')


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')
    likes = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return f"{self.id} {self.author.user.username} {self.title}"


class AnswerManager(models.Manager):
    def get_top_answers(self, question):
        return self.filter(question=question).order_by('-likes')


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    likes = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f'{self.id} {self.profile.user.username} {self.question.title}'


class QuestionLikesManager(models.Manager):
    def check_like(self, profile, question):
        self.exists(profile=profile, question=question)


@pgtrigger.register(
    pgtrigger.Trigger(
        name='question_likes_update',
        level=pgtrigger.Row,
        when=pgtrigger.Before,
        operation=pgtrigger.Insert,
        func=f'''
            UPDATE {Question._meta.db_table}
            SET likes = likes + 1
            WHERE id = NEW.question_id;
            RETURN NEW;
        ''',
    )
)
class QuestionLikes(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questionsLikes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questionsLikes')

    objects = QuestionLikesManager()

    def __str__(self):
        return f'{self.id} {self.question.id} {self.profile.user.username}'


class AnswerLikesManager(models.Manager):
    def check_like(self, profile, answer):
        self.exists(profile=profile, answer=answer)


@pgtrigger.register(
    pgtrigger.Trigger(
        name='answer_likes_update',
        level=pgtrigger.Row,
        when=pgtrigger.Before,
        operation=pgtrigger.Insert,
        func=f'''
            UPDATE {Answer._meta.db_table}
            SET likes = likes + 1
            WHERE id = NEW.answer_id;
            RETURN NEW;
        ''',
    )
)
class AnswerLikes(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answerLikes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answerLikes')

    objects = AnswerLikesManager()

    def __str__(self):
        return f'{self.id} {self.answer.id} {self.profile.user.username}'
