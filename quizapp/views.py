import csv
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .utils import load_questions_from_tsv
from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
    return render(request, 'quizapp/index.html')

# トップページ表示
def index_view(request):
    return render(request, 'quizapp/index.html')

# 問題表示ビュー
@login_required
def question_view(request, q_number):
    questions = load_questions_from_tsv()
    total = len(questions)

    if q_number < 1 or q_number > total:
        return HttpResponseNotFound("問題が見つかりません")

    question = questions[q_number - 1]
    index_to_label = ['A', 'B', 'C', 'D']
    labeled_choices = [
        f"{label}. {choice}" for label, choice in zip(index_to_label, question['choices'])
    ]

    if request.method == 'POST':
        selected = request.POST.get('choice')
        print("選択された値:", selected)
        action = request.POST.get('action')

        if selected is not None:
            if 'answers' not in request.session:
                request.session['answers'] = {}
            request.session['answers'][str(q_number)] = selected
            request.session.modified = True
            print("現在のセッション内の回答:", request.session.get('answers'))

        if action == 'end':
            return redirect('quizapp:result')
        elif action == 'prev':
            return redirect('quizapp:question', q_number=q_number - 1)
        elif q_number < total:
            return redirect('quizapp:question', q_number=q_number + 1)
        else:
            return redirect('quizapp:result')

    return render(request, 'quizapp/question.html', {
        'question': question,
        'q_number': q_number,
        'total': total,
        'choices': labeled_choices,
        'selected_answer': request.session.get('answers', {}).get(str(q_number), "")
    })

# 結果表示ビュー
def result_view(request):
    questions = load_questions_from_tsv()
    answers = request.session.get('answers', {})
    score = 0
    results = []
    index_to_label = ['A', 'B', 'C', 'D']

    for i, q in enumerate(questions, start=1):
        str_i = str(i)
        user_answer_text = answers.get(str_i)

        correct_label = q['correct']
        try:
            correct_index = index_to_label.index(correct_label)
            correct_text = q['choices'][correct_index]
        except (ValueError, IndexError):
            correct_text = "(不明)"

        labeled_choices = [
            f"{label}. {choice}" for label, choice in zip(index_to_label, q['choices'])
        ]

        if user_answer_text:
            try:
                user_index = q['choices'].index(user_answer_text)
                user_label = index_to_label[user_index]
                user_text = user_answer_text
                user_answer = f"{user_label}. {user_text}"
            except ValueError:
                user_answer = None
        else:
            user_answer = None

        is_correct = (user_answer_text == correct_text)
        if is_correct:
            score += 1

        results.append({
            'question': q['question'],
            'choices': labeled_choices,
            'correct': f"{correct_label}. {correct_text}",
            'user_answer': user_answer,
            'explanation': q['explanation'],
        })

    return render(request, 'quizapp/result.html', {
        'score': score,
        'results': results,
    })
