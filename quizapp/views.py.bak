import csv
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .utils import load_questions_from_tsv

# トップページ表示
def index_view(request):
    return render(request, 'quizapp/index.html')

# 問題表示ビュー
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
        user_answer = answers.get(str_i)  # 実際の選択肢のテキスト
        correct_label = q['correct']     # 例: 'A'

        try:
            correct_index = index_to_label.index(correct_label)
            correct_text = q['choices'][correct_index]
        except (ValueError, IndexError):
            correct_text = "(不明)"

        try:
            user_index = q['choices'].index(user_answer)
            user_label = index_to_label[user_index]
            user_text = user_answer
        except ValueError:
            user_label = "未回答"
            user_text = "（未選択）"

        is_correct = (user_answer == correct_text)
        if is_correct:
            score += 1

        labeled_choices = [
            f"{label}. {choice}" for label, choice in zip(index_to_label, q['choices'])
        ]

        results.append({
            'question': q['question'],
            'choices': labeled_choices,
            'correct': f"{correct_label}. {correct_text}",
            'user_answer': f"{user_label}. {user_text}",
            'explanation': q['explanation'],
        })

    return render(request, 'quizapp/result.html', {
        'score': score,
        'results': results,
    })
