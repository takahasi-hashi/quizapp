from . import views
from django.urls import path
from django.shortcuts import redirect

app_name = 'quizapp'

urlpatterns = [
    path('question/<int:q_number>/', views.question_view, name='question'),
    path('result/', views.result_view, name='result'),
    path('', lambda request: redirect('quizapp:question', q_number=1)),  # 最初の問題へリダイレクト
]
