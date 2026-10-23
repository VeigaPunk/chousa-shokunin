import json,random,sys,os
n=int(sys.argv[1]); r=random.Random(5)
words=[''.join(r.choice('abcdefghij') for _ in range(r.randint(3,9))) for _ in range(5000)]
def text(nbytes):
    out=[];L=0
    while L<nbytes:
        w=r.choice(words); out.append(w); L+=len(w)+1
    s=' '.join(out)
    # newlines every ~80
    return '\n'.join(s[i:i+80] for i in range(0,len(s),80))
span=text(n).strip()
src='intro line here\n'+span+'\ntail line\n'
os.makedirs('root/src',exist_ok=True)
open('root/src/a.txt','w').write(src)
mut=span[:len(span)//2]+('X' if span[len(span)//2]!='X' else 'Y')+span[len(span)//2+1:]
with open('root/claims.jsonl','w') as f:
    f.write(json.dumps({"id":"c1","source":"src/a.txt","span":span,"expect":"supported"})+'\n')
    f.write(json.dumps({"id":"c2","source":"src/a.txt","span":mut,"expect":"unsupported"})+'\n')
print(len(span))
