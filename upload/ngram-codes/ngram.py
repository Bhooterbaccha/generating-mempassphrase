import sys,nltk
import requests
import re,time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def graph(content, start, end, smoothing):
    url = "https://books.google.com/ngrams/graph"
    datapoints=[]
    querystring = {"content":content,
                   "case_insensitive":"on",
                   "year_start":start,
                   "year_end":end,
                   "corpus":"17",
                   "smoothing":smoothing}

    page = requests.get(url, params=querystring)

    soup = BeautifulSoup(page.content, 'html.parser')

    data = []
    for paragraph in soup.find_all('script'):
        data.append(paragraph.string)
    if len(data)>5:
     graph = data[5] #data[7] contains all the graph's plotted points in percentages.
    else:
     return datapoints
    try:
        found = re.search('"timeseries": (.+?)], "pare', graph).group(1)
        #found = re.search('"timeseries": (.+?)], "pare', graph).group(1)    #Start & End of graph data
    except AttributeError:
        #print("Encountered an error! Here's the response from the page\n Response: {}".format(page.content)) # apply your error handling
        return  datapoints# Exit gracefully
    found=found.split(']}')[0]
    tokens = found.rstrip().replace('[', '').split(', ')
    datapoints = [float(datapoint) for datapoint in tokens]

    return datapoints

def ngram_viewer(content, start, end, smoothing):
    graph_plot = graph(content, start, end, smoothing)
    #print(graph_plot)
    if len(graph_plot)>0:
     return float(sum(graph_plot[-5:])/5)
    else:
     return 0

#if __name__ == '__main__':
fil=sys.argv[1]
with open(fil,'r') as r:
   l={}
   cont=r.read()
   cont=cont.split('\n')
   #time.sleep(5)
   #print(cont)
   for i in cont:
     #print(i)
     prob=1
     mylist = list(nltk.bigrams(i.split(' ')))
     for j in mylist:
       query=' '.join([w for w in j]).rsplit()
       p=ngram_viewer(query, 2003, 2008, smoothing=0)
       if p==0 or p==None:
         prob*=1e-9
       else:
         prob*=p
     print(i,prob)
     l[i]=prob
     time.sleep(5)
pickle.dump(l,open('dump-VAE.pkl','wb'))
