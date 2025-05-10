from . import views
from django.urls import path
from django.shortcuts import redirect

app_name = 'quizapp'

urlpatterns = [
    path('', views.index_view, name='index'),  # トップページを追加
    path('question/<int:q_number>/', views.question_view, name='question'),
    path('result/', views.result_view, name='result'),
]
