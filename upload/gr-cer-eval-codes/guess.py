import pickle,operator,sys
from itertools import islice
from decimal import Decimal
from bisect import bisect
import numpy as np
import pandas as pd
#get the diceware passphrase probabilities
fil=sys.argv[1]
with open(fil, 'rb') as handle:
    passprob = pickle.load(handle)
#store probabilities
probArr = list(passprob.values())
#sort the probabilities
probArr=sorted(probArr)[::-1]
#convert to a dictionary
probDict={k: v for k,v in enumerate(probArr)}
#create rank dictionary
rankDict={}
prrank={}
for i in range(len(probDict)):
  if probDict[i]==1:
    rankDict[i]=1
    prrank[str(probDict[i])]=rankDict[i]
    continue
  if i==0:
    rankDict[i]=1/(len(probDict)*probDict[i])
    prrank[str(probDict[i])]=rankDict[i]
  if i>0:
    if probDict[i]!=probDict[i-1]:
      rankDict[i]=rankDict[i-1]+1/(len(probDict)*probDict[i])
      prrank[str(probDict[i])]=rankDict[i]
    else:
      rankDict[i]=rankDict[i-1]
      prrank[str(probDict[i])]=rankDict[i]
rArray=list(rankDict.values())
data=[]
for k,v in prrank.items():
  for key, value in passprob.items():
    if value == float(k):
      data.append([key,k,v])
#print('done lists for dataframe')
df = pd.DataFrame(data, columns = ['Passphrase', 'Probability','Guess Rank'])
df['count']=df['Passphrase'].str.split().str.len()

print(df)
print('Median Guess Rank:')
print(np.log10(df["Guess Rank"].mean()))
print('\n\n\n')
#print(list(df["Guess Rank"]))
#df.to_pickle("./grseq/cerbconst/comp-swD0-5del0-8cerorig.pkl")
#df.to_pickle("30noconst.pkl")
#df.to_pickle('guessnewdice.pkl')
#df.to_pickle('./trdoffguess/4word-95.pkl')
#df.to_pickle("4word-mascara-g.pkl")
df.to_pickle("mmap-markov-g.pkl")
