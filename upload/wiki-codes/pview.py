import pageviewapi,sys,pickle

fil=sys.argv[1]
result=[]
with open(fil,'r') as r:
  cont=r.read()
  titledata=cont.split('\n')
  #print(titledata)
  for titles in titledata:
    views=0
    months=0
    title=titles.split('\t')
    try:
      res=pageviewapi.per_article('en.wikipedia', title[0], '2015010100', '2020010100',
                        access='all-access', agent='all-agents', granularity='monthly')
    except:
      print(title[0])
      pass
    for k,v in res.items():
      for it in v:
        months+=1
        views+=it['views']
    if months!=0:
      avgview=(views/months)
    else:
      continue
    #print(title[0],avgview)
    result.append([title[0],avgview])
print(result[:10])
result.sort(key=lambda x: x[1],reverse=True)
print(result[:10])
print(len(result))
with open('title-pview.pkl', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
