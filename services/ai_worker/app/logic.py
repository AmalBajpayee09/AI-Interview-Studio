"""Deterministic parsing/scoring and safe practice helpers."""
import ast
import math
import re
import time
from decimal import Decimal, InvalidOperation

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

def question_kind(question):
    """Older quizzes have no kind field. Preserve multi-answer legacy quizzes."""
    return question.get('kind') or ('multiple' if isinstance(question.get('correct'), list) else 'single')


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        result = Decimal(str(value).strip())
        return result if result.is_finite() else None
    except (InvalidOperation, ValueError):
        return None


def score(questions, answers, negative_marking=0.25):
    """Deterministic scoring for single, multiple and numerical practice answers."""
    total=0.; correct=0; incorrect=0; unanswered=0
    sections={}
    for q in questions:
        section=q.get('section') or 'General'
        section_data=sections.setdefault(section, {'correct':0,'incorrect':0,'unanswered':0,'score':0.,'maximum':0.})
        points=float(q.get('points', 1))
        section_data['maximum']+=points
        answer=answers.get(q['id'])
        missing=answer is None or answer=='' or answer==[]
        if missing:
            unanswered+=1; section_data['unanswered']+=1
            continue
        kind=question_kind(q)
        if kind=='numerical':
            value=_number(answer)
            expected=_number(q['correct'])
            tolerance=_number(q.get('tolerance', 0))
            matches=value is not None and expected is not None and tolerance is not None and abs(value-expected)<=tolerance
        else:
            actual=set(answer) if isinstance(answer,list) else {answer}
            expected=set(q['correct']) if isinstance(q['correct'],list) else {q['correct']}
            matches=actual==expected
        if matches:
            correct+=1;total+=points
            section_data['correct']+=1;section_data['score']+=points
        else:
            incorrect+=1;total-=points*negative_marking
            section_data['incorrect']+=1;section_data['score']-=points*negative_marking
    maximum=sum(float(q.get('points',1)) for q in questions)
    for entry in sections.values():
        attempted=entry['correct']+entry['incorrect']
        entry['accuracy_pct']=round(entry['correct']/attempted*100,2) if attempted else None
        entry['score']=round(entry['score'],2)
    return {'score':round(total,2),'maximum':maximum,'percent':round(max(0,total)/maximum*100,2) if maximum else 0,
            'correct':correct,'incorrect':incorrect,'unanswered':unanswered,'sections':sections}


def validate_assessment_questions(questions):
    """Validate custom quiz formats before storing answer keys on disk."""
    if not isinstance(questions,list) or not 1<=len(questions)<=200:
        raise ValueError('Assessment must contain 1–200 questions')
    identifiers=set()
    for i,q in enumerate(questions):
        if not isinstance(q,dict): raise ValueError(f'Question {i+1} must be an object')
        qid=q.get('id');stem=q.get('stem');correct=q.get('correct')
        if not isinstance(qid,str) or not qid or len(qid)>80 or qid in identifiers:
            raise ValueError(f'Question {i+1} has a missing, duplicate or invalid ID')
        identifiers.add(qid)
        if not isinstance(stem,str) or not 1<=len(stem)<=5000:
            raise ValueError(f'Question {qid} needs a nonempty stem')
        kind=question_kind(q)
        if kind not in ('single','multiple','numerical'):
            raise ValueError(f'Question {qid} has an unsupported kind')
        opts=q.get('options',[])
        if kind=='numerical':
            if opts not in ([],None): raise ValueError(f'Numerical question {qid} must not contain answer options')
            value=_number(correct); tolerance=_number(q.get('tolerance',0))
            if value is None or tolerance is None or tolerance<0 or tolerance>1000000:
                raise ValueError(f'Numerical question {qid} needs finite answer and valid tolerance')
        else:
            if not isinstance(opts,list) or not 2<=len(opts)<=8:
                raise ValueError(f'Question {qid} needs 2–8 options')
            labels=[]
            for opt in opts:
                if not isinstance(opt,dict) or not isinstance(opt.get('label'),str) or not opt.get('label') or not isinstance(opt.get('text'),str) or not opt['text'].strip() or len(opt['text'])>2000 or len(opt['label'])>20:
                    raise ValueError(f'Question {qid} contains an invalid option')
                labels.append(opt['label'])
            if len(set(labels))!=len(labels): raise ValueError(f'Question {qid} contains duplicate option labels')
            if kind=='multiple' and (not isinstance(correct,list) or not correct or any(not isinstance(v,str) for v in correct)):
                raise ValueError(f'Multiple-answer question {qid} needs an answer list')
            if kind=='single' and not isinstance(correct,str):
                raise ValueError(f'Single-answer question {qid} needs one answer label')
            correct_set=set(correct) if isinstance(correct,list) else {correct}
            if not correct_set or not correct_set.issubset(set(labels)):
                raise ValueError(f'Question {qid} has an invalid answer key')
        try:points=float(q.get('points',1))
        except (ValueError,TypeError):raise ValueError(f'Question {qid} has invalid points')
        if not math.isfinite(points) or not 0<points<=100:
            raise ValueError(f'Question {qid} points must be between 0 and 100')
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
