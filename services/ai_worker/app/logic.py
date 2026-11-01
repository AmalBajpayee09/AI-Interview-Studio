"""Deterministic parsing/scoring and safe practice helpers."""
import ast
import re
import time

QUESTION_WORDS = re.compile(r'\b(what|why|how|when|where|who|which|explain|design|implement|solve|compare|define|क्या|कैसे|क्यों)\b', re.I)

def classify(text):
    low=text.lower()
    if re.search(r'(^|\n)\s*[a-d][).]\s+.+',text,re.I): return 'mcq'
    if any(t in low for t in ['time complexity','algorithm','leetcode','function','def ','array','reverse linked','dynamic programming']): return 'coding'
    if any(t in low for t in ['design a system','design twitter','architecture','scale to','load balancer']): return 'system-design'
    if any(t in low for t in ['machine learning','neural network','overfitting','precision','recall','gradient']): return 'machine-learning'
    if any(t in low for t in ['tell me about yourself','describe a time','conflict','leadership']): return 'behavioural'
    return 'general'

def segment(text):
    text=' '.join(text.strip().split())
    if not text: return []
    chunks=re.split(r'(?<=[?!।])\s+(?=[A-Zअ-ह])',text)
    return [{'text':c,'is_question': bool(QUESTION_WORDS.search(c) or c.endswith(('?','？')))} for c in chunks if c]

def parse_mcq(text):
    pattern = r'(?m)^\s*([A-D])[).:]\s*(.+?)\s*$'
    items=re.findall(pattern,text,re.I)
    return {'stem': re.split(r'(?m)^\s*[A-D][).:]\s*',text,1)[0].strip(), 'options': [{'label':k.upper(),'text':v} for k,v in items]}

def score(questions,answers,negative_marking=0.25):
    total=0.; correct=0; incorrect=0; unanswered=0
    for q in questions:
        answer=answers.get(q['id'])
        if answer is None or answer=='': unanswered+=1; continue
        actual=set(answer) if isinstance(answer,list) else {answer}
        expected=set(q['correct']) if isinstance(q['correct'],list) else {q['correct']}
        if actual==expected: correct+=1; total+=float(q.get('points',1))
        else: incorrect+=1; total-=float(q.get('points',1))*negative_marking
    maximum=sum(float(q.get('points',1)) for q in questions)
    return {'score':round(total,2),'maximum':maximum,'percent':round(max(0,total)/maximum*100,2) if maximum else 0,'correct':correct,'incorrect':incorrect,'unanswered':unanswered}

def validate_assessment_questions(questions):
    """Validate configurable quizzes before saving answer keys to the database."""
    if not isinstance(questions,list) or not 1<=len(questions)<=200:
        raise ValueError('Assessment must contain 1–200 questions')
    identifiers=set()
    for i, q in enumerate(questions):
        if not isinstance(q,dict): raise ValueError(f'Question {i+1} must be an object')
        qid=q.get('id');stem=q.get('stem');opts=q.get('options');correct=q.get('correct')
        if not isinstance(qid,str) or not qid or len(qid)>80 or qid in identifiers:
            raise ValueError(f'Question {i+1} has a missing, duplicate or invalid ID')
        identifiers.add(qid)
        if not isinstance(stem,str) or not 1<=len(stem)<=5000:
            raise ValueError(f'Question {qid} needs a short nonempty stem')
        if not isinstance(opts,list) or not 2<=len(opts)<=8:
            raise ValueError(f'Question {qid} needs 2–8 options')
        labels=[]
        for opt in opts:
            if not isinstance(opt,dict) or not isinstance(opt.get('label'),str) or not isinstance(opt.get('text'),str) or not opt['text'].strip() or len(opt['text'])>2000 or len(opt['label'])>20:
                raise ValueError(f'Question {qid} contains an invalid option')
            labels.append(opt['label'])
        if len(set(labels))!=len(labels): raise ValueError(f'Question {qid} contains duplicate option labels')
        correct_set=set(correct) if isinstance(correct,list) and all(isinstance(v,str) for v in correct) else {correct} if isinstance(correct,str) else set()
        if not correct_set or not correct_set.issubset(set(labels)):
            raise ValueError(f'Question {qid} has an invalid answer key')
        try: points=float(q.get('points',1))
        except (ValueError,TypeError): raise ValueError(f'Question {qid} has invalid points')
        if not 0<points<=100: raise ValueError(f'Question {qid} points must be between 0 and 100')
    return True

def syntax_check(code,language='python'):
    if language!='python': return {'status':'unavailable','message':'Static syntax verification only supports Python currently; generated code is never executed.'}
    try:
        ast.parse(code)
        return {'status':'parsed','message':'Python AST parse passed. This does not prove logic correctness or hidden tests.'}
    except SyntaxError as e:
        return {'status':'syntax_error','message':f'Line {e.lineno}: {e.msg}'}

def communication_feedback(transcript,seconds):
    words=re.findall(r"\b[\w']+\b", transcript, re.UNICODE)
    filler=sum(1 for w in words if w.lower() in {'um','uh','like','actually','basically'})
    return {'words':len(words),'wpm':round(len(words)*60/max(1,seconds)),'fillers':filler,'feedback': 'Try shorter sentences and concrete examples.' if filler > 3 else 'Review clarity and natural pacing; accents are not scored.'}

PRACTICE_QUESTIONS=[
 {'id':'q1','stem':'Which data structure is FIFO?','options':[{'label':'A','text':'Stack'},{'label':'B','text':'Queue'},{'label':'C','text':'Tree'},{'label':'D','text':'Heap'}],'correct':'B','explanation':'Queues remove elements in first-in, first-out order.','section':'DSA'},
 {'id':'q2','stem':'What is the time complexity of binary search on a sorted array?','options':[{'label':'A','text':'O(n)'},{'label':'B','text':'O(n²)'},{'label':'C','text':'O(log n)'},{'label':'D','text':'O(1)'}],'correct':'C','explanation':'The search space halves each iteration.','section':'DSA'},
 {'id':'q3','stem':'Which metric is precision?','options':[{'label':'A','text':'TP / (TP + FP)'},{'label':'B','text':'TP / (TP + FN)'},{'label':'C','text':'TN / (TN + FP)'},{'label':'D','text':'(TP + TN) / All'}],'correct':'A','explanation':'Precision measures what fraction of positive predictions are correct.','section':'ML'},
 {'id':'q4','stem':'Which SQL clause filters aggregated groups?','options':[{'label':'A','text':'WHERE'},{'label':'B','text':'HAVING'},{'label':'C','text':'ORDER BY'},{'label':'D','text':'LIMIT'}],'correct':'B','explanation':'HAVING applies predicates after grouping.','section':'SQL'},
]
