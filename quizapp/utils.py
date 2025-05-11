import csv
import os
from django.conf import settings

def load_questions_from_tsv():
    filepath = os.path.join(settings.BASE_DIR, 'quizapp', 'data', 'questions.tsv')
    questions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')  # DictReaderを使用してヘッダーをキーに変換
        for row in reader:
            # \n を実際の改行に変換
            question_raw = row.get('question')
            if not question_raw:
                continue  # 不完全な行をスキップ
            question_text = question_raw.replace('\\n', '\n')

            questions.append({
                'id': row['id'],  # TSVのid列を取得
                'question': question_text,  # 改行済みのテキストを使う
                'choices': [row['choices_A'], row['choices_B'], row['choices_C'], row['choices_D']],  # 選択肢
                'correct': row['answer'],  # 答え
                'explanation': row['explanation'],  # 解説
            })
    return questions
