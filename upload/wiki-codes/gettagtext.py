import mwparserfromhell,sys,re,glob,nltk
import xml.etree.ElementTree as etree
from xml.dom import minidom
from nltk.tokenize import sent_tokenize
reg1 = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
reg2=re.compile('http\S+')
reg3=re.compile('[^0-9a-zA-Z .,!?]')
reg4=re.compile(' +')
def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t
linext=0
linless=0
with open('textdump1.txt','w') as w:
 for event, elem in etree.iterparse('enwiki-20201120-pages-articles-multistream.xml', events=('end',)):
   tag = strip_tag_name(elem.tag)
   #if event == 'start':
   if tag=='text':
     x=elem.text
     if x!=None:
      x=x.split('\n')
      for xl in x:
       if len(xl)>0:
          #if xl[0].isalpha():
          xl=re.sub(reg1,'',xl)
          xl=re.sub(reg2,'',xl)
          xl=re.sub(reg3,' ',xl)
          xl=re.sub(reg4,' ',xl)
          xl=sent_tokenize(xl)
          for line in xl:
            line=line.lstrip().rstrip()
            if line.endswith('.jpg') or line.endswith('.png') or 'cite' in line:
               linext+=1
               continue
            if line!='' and len(line.split())>2:
               line=line.encode("ascii", "ignore").decode().lower()
               if line[-1]!='.':
                line=line+'.'
               w.write(line+'\n')
            else:
               linless+=1
      w.write('<<-$->>')
      elem.clear()

print('Lines with extensions and citations')
print(linext)
print('Lines with less than three words')
print(linless)
