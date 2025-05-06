import csv

def load_questions_from_tsv(path='questions.tsv'):
    questions = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # skip header
        for row in reader:
            questions.append({
                'number': int(row[0]),
                'text': row[1],
                'choices': row[2:6],
                'answer': row[6],
                'explanation': row[7],
            })
    return questions
