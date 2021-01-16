from django.core.management.base import BaseCommand
from app.models import Question, Profile, Answer
from random import choice
from faker import Faker

f = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--fill_db', type=str)


    def fill_questions(self, cnt):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Question.objects.create(
                author_id=choice(profile_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                title=f.sentence()[:128],
                #likes=f.random_int(min=0, max=100),
                count_answers=f.random_int(min=0, max=10),
            )

    def fill_answers(self, cnt):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Answer.objects.create(
                author_id=choice(profile_ids),
                question_id=choice(question_ids),
                text='. '.join(f.sentences(f.random_int(min=2, max=5))),
                #likes=f.random_int(min=0, max=100),   не работает, надо по-другому лайки рандомить
            )

    def fill_profiles(self, cnt):
        for i in range(cnt):
            Profile.objects.create(
                name=f.sentence()[:10],
            )    

    def handle(self, *args, **options):
        ismall = 5
        imedium = 500
        ilarge = 5000
        for a in options:
            if (options[a] == 'small'):
                self.fill_profiles(ismall)
                self.fill_questions(ismall)
                self.fill_answers(ismall*10)
            
            if (options[a] == 'medium'):
                self.fill_profiles(imedium)
                self.fill_questions(imedium)
                self.fill_answers(imedium*10)

            if (options[a] == 'large'):
                self.fill_profiles(ilarge)
                self.fill_questions(ilarge)
                self.fill_answers(ilarge*10)
                
            