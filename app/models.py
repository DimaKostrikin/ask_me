from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=32, verbose_name='Имя профиля')
    #avatar = models.ImageField(upload_to='200.jpg',verbose_name='Аватарка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


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
    likes = models.IntegerField(verbose_name='Лайки')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class AnswerManager(models.Manager):
    def published(self):
        return self.filter(is_published=True)

class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    likes = models.IntegerField(verbose_name='Кол-во лайков')
    #question = models.ForeignKey('Question', on_delete=models.CASCADE)

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'