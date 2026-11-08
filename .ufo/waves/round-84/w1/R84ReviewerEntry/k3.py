import re,hashlib
S214='tree/corpus/captures/a640b15abf781e5c583d7088.txt'
S018='tree/corpus/captures/248b43277f376e437a356909.txt'
S023='tree/corpus/captures/f5545a194c06ab421875b047.txt'
def flat(p):
    t=open(p,encoding='utf-8',errors='replace').read()
    return ' '.join(t.split())
F={'S214':flat(S214),'S018':flat(S018),'S023':flat(S023)}
Q={'Q1':('S214','Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies.'),
'Q2':('S214','date when each source was last searched or consulted.'),
'Q3':('S214','Present the full search strategies for all databases, registers and websites, including any filters and limits used.'),
'Q4':('S214','Specify the methods used to decide whether a study met the inclusion criteria of the review'),
'Q5':('S214','Describe the results of the search and selection process, from the number of records identified'),
'Q6':('S018','aiming to link model outputs to supporting evidence to ensure traceability and verifiability'),
'Q7':('S018','Thereby, we focus on approaches that use citations, attribution, or quotations for evidence-based text generation.'),
'Q8':('S018','However, the field is fragmented due to inconsistent terminology, isolated evaluation practices, and a lack of unified benchmarks.'),
'Q9':('S023','A related resource from which the described resource is derived.'),
'Q10':('S023','Recommended practice is to describe the date, date/time, or period of time as recommended for the property Date, of which this is a subproperty.'),
'Q11':('S023','Date (often a range) of validity of a resource.'),
'Q12':('S023','Date that the resource became or will become available.')}
for q,(s,txt) in Q.items():
    print(f'{q} {s} located={txt in F[s]}')
# contradiction scan: S214 checklist remainder + S018 abstract remainder + S023 relevant sections
L214=open(S214,encoding='utf-8',errors='replace').read().splitlines()
for i,l in enumerate(L214):
    s=re.sub(r'\s+',' ',l).strip()
    if s and any(w in s.lower() for w in ['omit','only the final','without the']):
        print(f'S214 {i+1}: {s[:200]}')
print('S018 abstract remainder:')
L18=open(S018,encoding='utf-8',errors='replace').read().splitlines()
print(re.sub(r'\s+',' ',L18[75])[:2000])
