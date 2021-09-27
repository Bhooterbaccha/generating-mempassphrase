import urllib.request, json
import sys,nltk,time,pickle
from urllib.error import HTTPError

fil=sys.argv[1]
with open(fil,'r') as r:
  l={}
  missbigram=[]
  cont=r.read()
  cont=cont.split('\n')
  cont=cont[:100]
  for line in cont:
    p=1
    mylist = list(nltk.bigrams(line.split(' ')))
    for j in mylist:
      time.sleep(3)
      query='+'.join([w for w in j])
      quer=' '.join([w for w in j])
      try:
        with urllib.request.urlopen('https://books.google.com/ngrams/json?content='+query+'&year_start=2015&year_end=2019&corpus=26&smoothing=3&case_insensitive=true') as url:
          if url.getcode()==429:
            time.sleep(int(url.headers["Retry-After"]))
          data = json.loads(url.read().decode())
          #print(data)
      except HTTPError as e:
        data = e.read().decode()
      if len(data) == 0 or not data:
        if j not in missbigram:
          missbigram.append(quer)
        p*=1e-10
        continue
      for i in data:
        if i['type']=='CASE_INSENSITIVE' or i['type']=='NGRAM':
          if sum(i['timeseries'])==0:
            if j not in missbigram:
              missbigram.append(quer)
            p*=1e-10
          else:
            p*=float(sum(i['timeseries'])/5)
    print(line,p)
    l[line]=p
    time.sleep(2)
#pickle.dump(l,open('10kdump-dice.pkl','wb'))
f=open('miss.txt','w')
f.write('\n'.join(missbigram))
