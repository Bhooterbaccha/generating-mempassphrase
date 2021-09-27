from itertools import islice
import pkg_resources
from symspellpy import SymSpell

sym = SymSpell()
#dictpath = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym.load_dictionary('dict.txt', 0, 1, separator="$")
#sym.load_dictionary(dictpath, term_index=0, count_index=1)
with open('orig-pw.txt','r') as r:
  cont=r.read()
  cont=cont.split('\n')
  cont=[c for c in cont if c!='']

with open('pp-wikiED2.txt','w') as wr:
  for i in cont:
    ic=i.encode("ascii", "ignore").decode().lower()
    ic=''.join(filter(str.isalpha, ic))
    result = sym.word_segmentation(ic,max_edit_distance=2)
    if len(result.corrected_string.split(' '))>=3:
      #print(result.corrected_string)
      wr.write(result.corrected_string+'\n')
    #print("{}, {}, {}".format(result.corrected_string, result.distance_sum,
    #                        result.log_prob_sum))
    #print(result.corrected_string, i)
    '''
    if len(result.corrected_string.split(' '))>=3 and len(min(result.corrected_string.split(' '), key=len))>2:
      print(result.corrected_string)
      wr.write(result.corrected_string+'\n')
    '''
