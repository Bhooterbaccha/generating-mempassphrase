import sys,nltk,time,re,csv,pickle
nltk.download('words')
from nltk.corpus import words
from itertools import combinations
fil=sys.argv[1] #passwordlist
fil1=sys.argv[2] #names
#print(words.words())
lw=words.words()
count=0
pp=[]
with open(fil1,'r') as r1:
  cont=r1.read()
  cont=cont.split('\n')
  names=cont
  names=[nam.lower() for nam in names]
cities = pickle.load( open( 'cities.pkl' , "rb" ) )
countries = pickle.load( open( 'countries.pkl' , "rb" ) )
#places=cities+countries
gerunds = pickle.load( open( 'gerunds.pkl' , "rb" ) )
with open('gthan3.txt','w') as wr:
 with open('gt3passphrase.csv','w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(["Passphrase", "Original Password"])
  with open(fil,'r') as r: #proc-pw.txt
    cont=r.read()
    cont=cont.split('\n')
    for ic in cont:
      dic={}
      subs=[]
      k=[]
      originalpw=ic.encode("ascii", "ignore").decode()
      ic=ic.encode("ascii", "ignore").decode().lower()
      icc=''.join(filter(str.isalpha, ic))
      for w in lw:
        if w in ic and (len(w)>2):
          subs.append(w)
      for nam in names:
        if nam in ic:
          subs.append(nam)
      for city in cities:
        if city in ic:
          subs.append(city)
      for ger in gerunds:
        if ger in ic:
          subs.append(ger)
      for cy in countries:
        if cy in ic:
          subs.append(city)
      subs=list(set(subs))
      #length=len(ic)
      #res=[ic[i:j+1] for i in range(length) for j in range(i,length)]
      #print(ic, res)
      if len(subs)>=3:
        l =sorted(subs, key = len)
        #ss=[j for i, j in enumerate(l) if all(j not in k for k in l[i + 1:])]
        #print(l)
        #l.remove('')
        iccopy=ic
        l.reverse()
        l=[x for x in l if x]
        if len(l[0])<3:
          continue
        for ind in l:
          if ind in iccopy:
           k.append(ind)
           iccopy= re.sub(ind, '', iccopy)
        k1=[len(v) for v in k]
        if len(''.join(k)) == len(icc) and k1.count(2)<2 and len(k)>2:
          for i in k:
            dic[i]=icc.find(i)
          di=sorted(dic, key=dic.get)
          if ''.join(di)!=icc:
            continue
          if len(min(di, key=len))<3 or 'isa' in di or 'ismy' in di or 'ina' in di or 'ilo' in di:
            continue
          if 'ion' in di:
            x=di.index("ion")
            di[x-1:x+1]=[''.join(di[x-1:x+1])]
            print(' '.join(di),originalpw)
          if 'ess' in di:
            x=di.index("ess")
            di[x-1:x+1]=[''.join(di[x-1:x+1])]
            print(' '.join(di),originalpw)
          print(' '.join(di),originalpw)
          if len(di)<3:
            continue
          fin=[' '.join(di),originalpw]
          writer.writerow(fin)
          count+=1
          print(count)
          wr.write(' '.join(di)+'\n')
