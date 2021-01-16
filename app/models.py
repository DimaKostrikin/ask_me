from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class Profile(models.Model):
    name = models.CharField(max_length=32, verbose_name='Имя профиля')
    #avatar = models.ImageField(upload_to='200.jpg',verbose_name='Аватарка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

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

class Question(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок вопроса')
    text = models.TextField(verbose_name='Текст вопроса')
    tag = models.CharField(max_length=16, verbose_name='Тэг вопроса')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    likes = GenericRelation('Like')

    date = models.DateField(auto_now_add=True, verbose_name="Дата вопроса")
    
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    count_answers = models.IntegerField(verbose_name='Кол-во ответов')

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
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
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