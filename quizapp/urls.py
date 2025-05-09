from . import views
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

app_name = 'quiz'

urlpatterns = [
    path('question/<int:q_number>/', views.question_view, name='question'),
    path('result/', views.result_view, name='result'),
    path('', lambda request: redirect('quiz/', permanent=True)),
    path('quiz', lambda request: redirect('quiz/', permanent=True)),  # スラッシュなし→ありにリダイレクト
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
    #path('explanation/', views.explanation_view, name='explanation'),
]
