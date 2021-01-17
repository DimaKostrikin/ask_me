from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    nickname = models.CharField(max_length=32, verbose_name='Имя профиля', default="")
    email = models.EmailField(max_length=254, verbose_name='Электронная почта', default="")
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', verbose_name='Аватарка', default='200.jpg')
    rate = models.IntegerField(default=0, verbose_name="Rate")
    
    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=32, verbose_name='Имя тега')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class QuestionManager(models.Manager):
    def published(self):
        return self.filter(is_published=True)
    def tag(self, tag_1):
        return self.filter(tag=tag_1)
    def best(self):
        return self.exclude(likes=0)
    def one(self, num):
        return self.filter(id=num)
    def get_by_id(self, qid):
        return self.get(id=qid)
    def find_id(self, question_id):
        return self.get(id=question_id)
    def find_tag(self, tag):
        return self.filter(tags__word__icontains=tag)

class Question(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок вопроса')
    text = models.TextField(verbose_name='Текст вопроса')
    tag = models.CharField(max_length=16, verbose_name='Тэг вопроса')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    likes = GenericRelation('Like')

    date = models.DateField(auto_now_add=True, verbose_name="Дата вопроса")
    rate = models.IntegerField(default=0, verbose_name="Rate")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    count_answers = models.IntegerField(verbose_name='Кол-во ответов', default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class AnswerManager(models.Manager):
    def get_id(self, answer_id):
        return self.get(id=answer_id)

    def count(self, question_id):
        return self.filter(question = question_id).count()

    def get_by_q(self, question_id):
        return self.filter(question = question_id)

class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    likes = GenericRelation('Like')

    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, verbose_name="Rate")
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name="Дата вопроса")
    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Like(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Dislike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class RatingManagerQuestions(models.Manager):
    def find_id(self, id):
        return self.get(id=id)

    def find_eu(self, element, user):
        return self.filter(to=element).filter(user=user)

    def change_rate(self, qid, user, action):
        question = Question.objects.find_id(qid)
        rate = RatingQuestions.objects.create(user=user, to=question)
        rate.save()
        if action == "like":
            question.rate += 1
        else:
            question.rate -= 1
        question.save()
        return question.rate

class RatingUsers(models.Model):
    user = models.ForeignKey('Profile', related_name="user_profile", on_delete=models.CASCADE, 
        verbose_name="User")
    to = models.ForeignKey('Profile', related_name="rated_user",on_delete=models.CASCADE, 
        verbose_name="Rated user")
    #objects = RatingManager()

    class Meta:
        verbose_name = "Users' rating"
        verbose_name_plural = "Users' ratings"

class RatingQuestions(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, 
        verbose_name="Users")
    to = models.ForeignKey('Question', on_delete=models.CASCADE, 
        verbose_name="Questions")
    objects = RatingManagerQuestions()

    def __str__(self):
        return "rate"

    class Meta:
        verbose_name = "Questions' rating"
        verbose_name_plural = "Questions' ratings"

class RatingAnswers(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, 
        verbose_name="User")
    to = models.ForeignKey('Answer', on_delete=models.CASCADE, 
        verbose_name="Answer")
    #objects = RatingManager()

    class Meta:
        verbose_name = "Answers' rating"
        verbose_name_plural = "Answers' ratings"