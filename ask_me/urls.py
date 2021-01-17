"""ask_me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hot/', views.hot_questions, name='hot-questions-view'),
    path('new/', views.new_questions, name='new-questions-view'),
    path('login/', views.login_page, name='login-view'),
    path('logout/', views.logout, name='logout-view'),
    path('settings/', views.settings_page, name='settings-view'),
    path('', views.new_questions, name='home-view'),
    path('ask/', views.ask_question, name='ask-view'),
    path('question/<int:pk>/', views.question, name='one-question-view'),
    path('tag/<str:pk>', views.tagged_questions, name='tag-view'),
    path('signup/', views.signup_page, name='signup'),
    path('vote/', views.vote, name='vote'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)