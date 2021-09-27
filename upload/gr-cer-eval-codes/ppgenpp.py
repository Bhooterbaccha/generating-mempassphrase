from __future__ import print_function
import sys,re,nltk,csv
import random,os,pickle,time
from collections import defaultdict
import numpy as np
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
import statistics
import pronouncing,syllables

vocab=pickle.load(open('unigram-5p.pkl','rb'))
markov_graph=pickle.load(open('wiki5pcombined-word.pkl','rb'))
#markov_graph_pos=pickle.load(open('wiki5pcombined-pos.pkl','rb'))
voc=dict(vocab)
sum=0
for k,v in voc.items():
  #voc[k]=v/40461941
  voc[k]=v/len(voc)
miss=[]
bigmiss=[]
count=0


def getprob(s):
  global count,xdic
  bpresent=0
  sproc='<begin> '+s.rstrip()+' <end>'
  x=len(list(markov_graph['<begin>'].keys()))
  prob=1
  flag=0
  p1={}
  pp1={}
  bigr=list(sproc.split(" "))
  for i in range(len(bigr)-1):
    count+=1
    key=' '.join(bigr[i:i+1])
    if key in markov_graph:
      gram=key+' '+bigr[i+1]
      norm=np.array(list(markov_graph[key].values()),dtype=np.float64).sum()
      if i+1<len(bigr):
        if bigr[i+1] in list(markov_graph[key].keys()):
           choices=list(markov_graph[key].keys())
           weights = np.array(list(markov_graph[key].values()),dtype=np.float64)
           weights /= weights.sum()
           for c in range(len(choices)):
             p1[choices[c]]=weights[c]
           prob*=p1[str(bigr[i+1])]
        else:
           bigmiss.append(gram)
           bpresent+=1
           if bigr[i+1] in voc:
             prob*=voc[bigr[i+1]]
           else:
             miss.append(bigr[i+1])
             prob*=1/norm
    else:
      if key in voc:
         prob*=voc[key]
      else:
         flag=1
         prob*=1/len(markov_graph)
  if bpresent>=0 and flag==0:
    if prob in xdic.keys():
      xdic[prob].append(s.rstrip())
    else:
      xdic[prob]=[]
      xdic[prob].append(s.rstrip())
    return prob
  else:
    return prob

fil=sys.argv[1]
'''
xdic={}
cl=pickle.load(open('newlenpp.pkl','rb'))
with open(fil,'r') as r:
  l={}
  cont=r.read()
  cont=cont.split('\n')
  #print(cont)
  fl=0
  for s in cont:
   if len(cl)>(fl):
    if cl[fl]<=len(s.split(' ')):
      s=' '.join(s.split()[:cl[fl]])
      s=s.lower()
      if len(s.split())>1:
       probability=getprob(s)
       print(s,probability)
       l[s]=probability
       fl+=1
    else:
       if len(s.split())>1:
         probability=getprob(s)
         print(s,probability)
         l[s]=probability
         fl+=1
print(len(l))
#pickle.dump(l,open('./probseq/cerbconst/swD0-5del0-8cerorig.pkl','wb'))
pickle.dump(l,open('m-mascara.pkl','wb'))

#print(xdic)
#pickle.dump(xdic,open('prob-seq1r.pkl','wb'))
'''
lenpp={}
tw=[]
tbig=0
xdic={}
with open(fil,'r') as r:
  l={}
  cont=r.read()
  cont=cont.split('\n')
  cont=[i.lower() for i in cont if i!='']
  fl=0
  for s in cont:
    if len(s.split())>1 and len(l)<1000:
       tw.extend(s.split())
       tbig+=len(s.split(' '))+1
       probability=getprob(s)
       #print(probability)
       if probability!=0:
         l[s]=probability
         lenpp[s]=len(s.split(' '))
         print(s,l[s])
    else:
      break
print(len(lenpp))
#pickle.dump(list(lenpp.values()),open('lenofpp.pkl','wb'))
#pickle.dump(l,open('./probseq/30-nwUB.pkl','wb'))
#pickle.dump(l,open('./trdoffprob/4word-60.pkl','wb'))
#pickle.dump(l,open('./probseq/cerbconst/comp-swD0-5del0-8cerorig.pkl','wb'))
#pickle.dump(l,open('4word-mmap.pkl','wb'))
pickle.dump(l,open('mmap-markov.pkl','wb'))
'''
print(xdic)
'''
