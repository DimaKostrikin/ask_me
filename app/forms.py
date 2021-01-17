from django import forms
from app.models import Question, Profile, Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea
from crispy_forms.helper import FormHelper

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class SignUpForm(UserCreationForm):
    nickname = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'password1', 'password2']

    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        if user:
            msg = u"This username has already been taken!"
            self._errors["username"] = self.error_class([msg])
            del self.cleaned_data["username"]
        profile = Profile.objects.filter(email=self.cleaned_data.get('email'))
        if profile:
            msg = u"This email has already been taken!"
            self._errors["email"] = self.error_class([msg])
            del self.cleaned_data["email"]

        return self.cleaned_data

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.refresh_from_db()  # load the profile instance created by the signal
        user.profile.nickname = self.cleaned_data.get('nickname')
        user.profile.email = self.cleaned_data.get('email')
        user.profile.save()
        return user


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):

	class Meta:
		model = Answer
		fields = ['text']

		widgets = {
            'text': Textarea(attrs={'cols': 60,'rows': 8}),
        }

	def __init__(self, *args, **kwargs):
		self.profile = kwargs.pop('profile',None)
		self.qid = kwargs.pop('qid',None)
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False

	def save(self, *args, **kwargs):
		answer = super().save(*args, **kwargs, commit=False)
		answer.author = self.profile
		answer.question = self.qid
		answer.save()
		return answer

class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user

