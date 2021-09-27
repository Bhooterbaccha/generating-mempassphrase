import sys,re,nltk,csv
import random,pickle
from collections import defaultdict
import numpy as np

d=pickle.load(open('unigram-5p.pkl','rb'))
d=dict(d)
val=list(d.values())
hp = np.percentile(val, 95)
lp = np.percentile(val, 5)
print(hp,lp)
wordlist=[]
for k,v in d.items():
        if v>lp and v<hp:
                wordlist.append(k)
c1=0

with open('dice-4word.txt','w') as w:
        while c1<1000:
                flag=0
                c=random.choices(wordlist,k=4)
                for i in c:
                        if i.isalpha() and len(i)>=3:
                                continue
                        else:   
                                flag=1
                st=' '.join(c)
                try:
                        st.encode('ascii')
                except UnicodeEncodeError:
                        pass
                else: 
                        if flag!=1:
                                  w.write(st+'\n')
                                  c1+=1
c2=0

with open('dice-5word.txt','w') as w:
        while c2<1000:
                flag=0
                c=random.choices(wordlist,k=5)
                for i in c:
                        if i.isalpha() and len(i)>=3:
                                continue
                        else:   
                                flag=1
                st=' '.join(c)
                try:
                        st.encode('ascii')
                except UnicodeEncodeError:
                        pass
                else: 
                        if flag!=1:
                                  w.write(st+'\n')
                                  c2+=1

