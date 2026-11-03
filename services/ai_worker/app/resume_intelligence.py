"""Source-grounded resume section analysis. No inferred achievements or fabricated facts."""
from __future__ import annotations
import re

HEADINGS={
 'skills':r'(?:technical\s+)?skills|technologies',
 'education':r'education|academics|qualifications',
 'experience':r'(?:work\s+)?experience|employment|internships?',
 'projects':r'(?:selected\s+)?projects?|portfolio',
 'achievements':r'achievements?|awards?|certifications?',
}
LABELS=[(kind,re.compile(r'^\s*(?:#{1,3}\s*)?(?:'+pattern+r')\s*:?\s*$',re.I)) for kind,pattern in HEADINGS.items()]

def sections(text:str,document_id:str)->dict:
    lines=text[:50000].splitlines()[:900]
    found=[];kind=None;start=None;body=[]
    def flush(end):
        if kind is None or not body:return
        excerpt='\n'.join(body).strip()
        if excerpt:
            found.append({'kind':kind,'source':{'document_id':document_id,'start_line':start,'end_line':end},
                          'excerpt':excerpt[:1200],'excerpt_truncated':len(excerpt)>1200})
    for number,line in enumerate(lines,1):
        heading=next((key for key,pattern in LABELS if pattern.match(line)),None)
        if heading:
            flush(number-1);kind=heading;start=number+1;body=[]
        elif kind and line.strip():
            body.append(line.strip())
    flush(len(lines))
    questions=[]
    for section in found:
        if section['kind']!='projects':continue
        candidates=[line.strip(' -•*\t') for line in section['excerpt'].splitlines() if line.strip()]
        for candidate in candidates[:3]:
            label=re.split(r'\s+[–—-]\s+|\s*[:|]\s*',candidate)[0][:90].strip()
            if not (3<=len(label)<=90):continue
            questions.append({'question':f'Walk through the architecture, your specific contribution, and trade-offs for the project described as: {label}',
                              'source':section['source'],'type':'grounded_practice_prompt'})
        break
    return {'document_id':document_id,'sections':found,'questions':questions[:3],
            'covered_categories':sorted({x['kind'] for x in found}),
            'missing_categories':sorted(set(HEADINGS)-{x['kind'] for x in found}),
            'source_grounded':True,
            'note':'Only headings and excerpts from supplied text are extracted. Claims are not independently verified.'}
