from __future__ import print_function
import sys,re,nltk,csv
import random,os,pickle,time
from collections import defaultdict
import numpy as np
import pandas as pd
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
import statistics
import pronouncing,syllables

vocab=pickle.load(open('unigram-5p.pkl','rb'))

voc=dict(vocab)
count=0

sortednames=sorted(voc.keys(), key=lambda x:x.lower())
indexdict={}
indval=0
for i in sortednames:
  if len(i)>=3 and voc[i]>1:
    indexdict[i]=indval
    indval+=1

def getguess(s):
  gr=0
  words=s.split()
  words=words[::-1]
  k=len(words)
  for i in range(k):
    gr+=indexdict[words[i]]*len(indexdict)**i
  return gr

def getprob(s):
  k=len(s.split())
  p=(1/len(indexdict))**k
  return p

fil=sys.argv[1]
data=[]
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
       guess=getguess(s)
       prob=getprob(s)
       print(s,prob,guess)
       data.append([s,prob,guess])
       fl+=1
    else:
       if len(s.split())>1:
         guess=getguess(s)
         prob=getprob(s)
         print(s,prob,guess)
         data.append([s,prob,guess])
         fl+=1
df = pd.DataFrame(data, columns = ['Passphrase', 'Probability','Guess Rank'])
print(df)
df.to_pickle('dicen.pkl')
