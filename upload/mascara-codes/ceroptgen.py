import sys,re,nltk,csv
import random,pickle,time
from collections import defaultdict
import numpy as np
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import phrasemachine,statistics

markov_graph=pickle.load(open('bigram.pickle','rb'))
markov_graph_pos=pickle.load(open('bigram-pos.pickle','rb'))
#pos_map_word=pickle.load(open('pos-word.pickle','rb'))
stopword = set(stopwords.words('english'))
ppsize=pickle.load(open('newlenpp.pkl','rb')) #an array of passphrase lengths required
#endcheck=pickle.load(open('trigram.pkl','rb'))

d=pickle.load(open('unigram-5p.pkl','rb'))
d=dict(d)
s=sum(list(d.values()))
print(s)

for k,v in d.items():
  d[k]=v/s
bigramdict=pickle.load(open('biprob.pkl','rb'))
def sdc(string):
  lis=[len(k) for k in string.split(' ')]
  sd=statistics.stdev(lis)
  mean=statistics.mean(lis)
  return sd/mean

def cal(x,y):
  z= (-3.4279e-02*x-6.4687e-03*y)
  return z

def makesent(markov_graph,markov_graph_pos,size,prob):
    l=[]
    oldwords=''
    while len(' '.join(oldwords))<3 or ' '.join(oldwords).isdigit() or ' '.join(oldwords) in stopword:
      #oldwords =  random.choice(list(markov_graph['<begin>'].keys())).split()
      w1 = np.array(list(markov_graph['<begin>'].values()),dtype=np.float64)
      w1 /= w1.sum()
      c = list(markov_graph['<begin>'].keys())
      oldwords = np.random.choice(c,p=w1).split()
      ind=c.index(oldwords[0])
    prob=w1[ind]
    #print(prob)
    string = ' '.join(oldwords) + ' '
    while True:
        try:
            key = ' '.join(oldwords)
            flag=0
            l=[]
            choices = list(markov_graph[key].keys())
            if '<end>' in choices and string.split()[-1] not in stopword and len(string.split())>=size:
              prob*=1/len(choices)
              break
            keys=[key+' '+i for i in choices]
            weights=np.array([np.log(bigramdict[i])for i in keys])
            #print(weights)
            weightunig=np.array([np.log(d[c]) for c in choices])
            #1.1966e-04*sdchar[i]
            #sdchar=np.array([sdc(string+' '+i) for i in choices])
            #jointw=np.array([1-(1.1966e-04*sdchar[i]-3.4279e-02*weightunig[i]-6.4687e-03*weights[i]) for i in range(len(weights))])
            jointw=np.array([(-3.4279e-02*weightunig[i]-6.4687e-03*weights[i]) if weights[i]<(0.8*-(17.4))\
                    and cal(weightunig[i],weights[i])<=0.5 else 0\
                    for i in range(len(weights))])
            #jointw=np.array([(-3.4279e-02*weightunig[i]-6.4687e-03*weights[i]) for i in range(len(weights))])
            #print(jointw)
            if jointw.sum()==0:
              break
            jointw /= jointw.sum()
            if len(jointw)>1 and 1 not in jointw:
              #print(jointw)
              jointw=np.array([1-i if i>0 else 0 for i in jointw])
              jointw /= jointw.sum()
            lisjoin=[i for i in jointw if i!=0]
            newword=''
            tries=0
            while len(newword)<3 or newword.isdigit():
              newword = np.random.choice(choices,p=jointw)
              tries+=1
              if tries>5 or newword=='<end>':
                prob*=1/len(lisjoin)
                break
            if newword.isalpha() and len(newword)>=3:
              string += newword + ' '
              prob*=1/len(lisjoin)
            if len(string.split())>=size:
              prob*=1/len(lisjoin)
              break
            oldwords[:]=oldwords[1:]
            oldwords.append(newword)
        except KeyError:
            #string = 'error'
            return string,prob
    return string,prob

c=0
rej=[]
dic={}
with open('6word-opt.txt','w') as w: 
  start_time = time.time()
  countrej=0
  while c<1000:
    #print(ppsize[c])
    p=1
    countrej+=1
    string,prob = makesent(markov_graph,markov_graph_pos,6,p) #call to generate passphrase, we don't use pos here.
    string=string.replace("<begin>", "").replace("<end>", "").strip()
    #print(string)
    if len(string.split()) != 6:
      continue
    #string=' '.join(string.split()[:ppsize[c]])
    ke=' '.join(string.split()[-2:])
    #print(ke)
    #print(endcheck[ke].keys())
    liskey=dict(phrasemachine.get_phrases(string)['counts']).keys()
    #if string.split()[-1] not in stopword and ke in endcheck.keys() and ke in list(liskey) and '<end>' in list(endcheck[ke].keys()):
    if string in list(liskey) and string.split()[-1] not in stopword:
      try:
        string.encode('ascii')
      except UnicodeEncodeError:
        #print(string)
        pass
      else:
        print(string,prob)
        w.write(string+'\n')
        c+=1
        dic[string]=prob
        rej.append(countrej-1)
        countrej=0
  print("--- %s seconds ---" % (time.time() - start_time))
#pickle.dump(dic,open('sw-prob.pkl','wb'))
print(statistics.mean(rej))
print(statistics.median(rej))
