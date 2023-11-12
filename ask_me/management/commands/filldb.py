from django.core.management.base import BaseCommand
from django.contrib.auth import hashers
from ask_me.models import *


class Command(BaseCommand):
    help = '''Fills db with ratio:
            - ratio tags
            - ratio users
            - ratio*10 questions
            - ratio*100 answers
            - ratio*200 likes'''

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int, help='Ratio value')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio'][0]

        TAGS_RATIO = ratio
        USERS_RATIO = ratio
        QUESTIONS_RATIO = 10 * ratio
        ANSWERS_RATIO = 100 * ratio
        QLIKES_RATIO = 200 * ratio
        ALIKES_RATIO = 200 * ratio

        first_tag_id = Tag.objects.last().id + 1
        first_user_id = User.objects.last().id + 1
        first_profile_id = Profile.objects.last().id + 1
        first_question_id = Question.objects.last().id + 1
        first_answer_id = Answer.objects.last().id + 1
        first_question_likes_id = QuestionLikes.objects.last().id + 1
        first_answer_likes_id = AnswerLikes.objects.last().id + 1

        tags = [Tag(name=f'Tag{tag_id}')
                for tag_id in range(first_tag_id, first_tag_id + TAGS_RATIO)]
        Tag.objects.bulk_create(tags)

        users = [User(username=f'User{user_id}',
                      first_name=f'firstName{user_id}',
                      last_name=f'lastName{user_id}',
                      email=f'user{user_id}@mail.ru',
                      password=hashers.make_password(f'pass{user_id}'))
                 for user_id in range(first_user_id, first_user_id + USERS_RATIO)]
        User.objects.bulk_create(users)

        profiles = [Profile(user_id=user_id)
                    for user_id in range(first_user_id, first_user_id + USERS_RATIO)]
        Profile.objects.bulk_create(profiles)

        questions = [Question(author_id=first_profile_id + question_id % USERS_RATIO,
                              title=f'Title of question #{question_id}',
                              body=f'Body of question #{question_id}')
                     for question_id in range(first_question_id, first_question_id + QUESTIONS_RATIO)]
        Question.objects.bulk_create(questions)
        for i in range(len(questions)):
            for j in range(3):
                questions[i].tags.add(tags[(i - 2) % TAGS_RATIO + j])

        answers = [Answer(profile_id=first_profile_id + answer_id % USERS_RATIO,
                          question_id=first_question_id + answer_id % QUESTIONS_RATIO,
                          body=f'Some cool answer number№{answer_id}')
                   for answer_id in range(first_answer_id, first_answer_id + ANSWERS_RATIO)]
        Answer.objects.bulk_create(answers)

        questions_likes = [QuestionLikes(profile_id=first_profile_id + like_id % USERS_RATIO,
                                         question_id=first_question_id + like_id % QUESTIONS_RATIO)
                           for like_id in range(first_question_likes_id, first_question_likes_id + QLIKES_RATIO)]

        QuestionLikes.objects.bulk_create(questions_likes)

        answers_likes = [AnswerLikes(profile_id=first_profile_id + like_id % USERS_RATIO,
                                     answer_id=first_answer_id + like_id % ANSWERS_RATIO)
                         for like_id in range(first_answer_likes_id, first_answer_likes_id + ALIKES_RATIO)]

        AnswerLikes.objects.bulk_create(answers_likes)
