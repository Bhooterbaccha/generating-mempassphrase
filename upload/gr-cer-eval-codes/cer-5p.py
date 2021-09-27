import pandas as pd
import numpy as np
import statistics,string
import nltk,pickle,sys

def get_unigram_probability(word, fdist, vocab_size, total_words, smoothing_factor):
	unigram_probability = np.log((fdist[word] + smoothing_factor) / (total_words + (smoothing_factor * vocab_size)))
	return unigram_probability      

def calculate_unigram_freq_of_sentence_token_list(tokens, fdist, vocab_size, total_words, smoothing_factor):       
	prob_list = []
	prob = 0.0
	for word in tokens:
		unigram_probability = get_unigram_probability(word, fdist, vocab_size, total_words, smoothing_factor)
		prob_list.append(unigram_probability)
	for i in range(len(prob_list)):
		prob = prob + prob_list[i]
	return prob

def get_bigram_probability(first, second, cfd, fdist, smoothing_factor, vocab_size):
	bigram_frequency = cfd[first][second]
	unigram_frequency = fdist[first]
	bigram_probability = np.log(( bigram_frequency  + smoothing_factor) / ( unigram_frequency + smoothing_factor * vocab_size))
	return bigram_probability

def calculate_bigram_freq_of_sentence_token_list(tokens, cfd, fdist, smoothing_factor, vocab_size):
	prob_list = []
	prob = 0.0
	## assume that 'START' precedes the first token
	previous = '<begin>'
	for token in tokens:
		next_probability = get_bigram_probability(previous, token, cfd, fdist, smoothing_factor, vocab_size)
		#print(previous,',',token,'-->',(float('%.3g' % next_probability)))
		prob_list.append(next_probability)
		previous = token
	## assume that 'END' follows the last token
	next_probability = get_bigram_probability(previous,'<end>', cfd, fdist, smoothing_factor, vocab_size)
	#print(previous, ',', '<end>', '-->', next_probability)
	prob_list.append(next_probability)
	#probability = multiply_list(prob_list)
	#print('Total Probability',float('%.3g' % probability))
	for i in range(len(prob_list)):
		prob = prob + prob_list[i]
	return prob

def get_trigram_probability(first, second, third, cfd, cfdt, vocab_size, smoothing_factor):
	trigram_frequency = cfdt[first, second][third]
	bigram_frequency = cfd[first][second]
	#unigram_frequency = fdist2[first]
	bigram_probability = np.log(( trigram_frequency  + smoothing_factor) / ( bigram_frequency + smoothing_factor * vocab_size))
	return bigram_probability

def calculate_trigram_freq_of_sentence_token_list(tokens, cfd, cfdt, vocab_size, smoothing_factor):		
	prob_list = []
	prob = 0.0
	## assume that 'START' precedes the first token
	prev_prev = '<begin>'
	previous = tokens[0]
	for token in tokens[1:]:
		next_probability = get_trigram_probability(prev_prev, previous, token, cfd, cfdt, vocab_size, smoothing_factor)
		prob_list.append(next_probability)
		prev_prev = previous
		previous = token
	## assume that 'END' follows the last token
	next_probability = get_trigram_probability(prev_prev, previous, '<end>', cfd, cfdt, vocab_size, smoothing_factor)
	prob_list.append(next_probability)
	for i in range(len(prob_list)):
		prob = prob + prob_list[i]
	return prob

def cer1(nw,sdchar,oov,lprob1):
  cer=0.47008*nw + 0.14598*oov + -0.000014009*sdchar - 0.13409*lprob1 - 0.9658
  #cer=-11.65 + (0.83*nw)+(0.48*sdchar)+(6.94*oov)-(1.00*lprob1)
  return cer

def cer2(nw,sdchar,oov,lprob1,lprob2):
  cer= 1.7637e-01*nw + 3.3935e-01*oov + 1.1966e-04*sdchar -3.4279e-02*lprob1 -6.4687e-03*lprob2- 1.4066
  #cer= 0.0788*nw + 0.1412*oov + 0.0004*sdchar - 0.0295*lprob1 - 0.0791*lprob2 - 1.4066
  return cer

def cer3(nw,sdchar,oov,lprob1,lprob2,lprob3):
  cer= 0.00012631*nw + 0.23503*oov + 0.00063031*sdchar -0.056929*lprob1 - 0.020415*lprob2 - 0.046033*lprob3 - 1.1753
  return cer

if __name__ == '__main__':
	fil=sys.argv[1]
	smoothing_factor=1
	word_list=[]
	f=open("wlist_wsj64k.txt","r")
	for line in f:
		word_list.append(line.strip().lower())
	vocab=pickle.load(open('./grampkl/vocab-5p.pkl','rb'))
	fdist=pickle.load(open('./grampkl/unigram-5p.pkl','rb'))
	cfd=pickle.load(open('./grampkl/bigram-5p.pkl','rb'))
	cfdt=pickle.load(open('./grampkl/trigram-5p.pkl','rb'))
	vocab_size=len(vocab)
	total_words=40461941
	df=pd.read_pickle(fil)
	#gr=df['Guess Rank'].tolist()
	gr=df['GuessRank'].tolist() #for MMAP
	#fil=df['Passphrase'].tolist()
	fil=df['phrase'].tolist() #for MAP
	text=[]
	nw=[]
	oov=[]
	sdchar=[]
	lprob1=[]
	lprob2=[]
	lprob3=[]
	for line in fil:
		line=' '.join(line.split(' ')[:6])
		w=line.lower().strip().split(" ")
		arr=[]
		oov_p=0
		if len(w)<3:
			continue
		for k in w:
			if((len(k)==1 and (k=="i" or k=="a")) or len(k)>1):
				arr.append(len(k))
			if k not in word_list:
				oov_p+=1
		if (len(arr)>1):
			sd=statistics.stdev(arr)
		else:
			continue
		text.append(line.strip())
		nw.append(len(' '.join(w)))
		sdchar.append(sd)
		oov.append(float(oov_p/len(w)))
		lprob1.append(calculate_unigram_freq_of_sentence_token_list(w, fdist, vocab_size, total_words, smoothing_factor))
		lprob2.append(calculate_bigram_freq_of_sentence_token_list(w, cfd, fdist, smoothing_factor, vocab_size))
		lprob3.append(calculate_trigram_freq_of_sentence_token_list(w, cfd, cfdt, vocab_size, smoothing_factor))
	dff=pd.DataFrame()
	dff["pass"]=text
	dff["nw"]=nw
	dff["oov"]=oov
	dff["sdchar"]=sdchar
	dff["lprob1"]=lprob1
	dff["lprob2"]=lprob2
	dff["lprob3"]=lprob3
	dff["GuessRank"]=gr
	cerv1=[]
	cerv2=[]
	cerv3=[]
	for i,ind in dff.iterrows():
		cerv1.append(cer1(ind["nw"],ind["sdchar"],ind["oov"],ind["lprob1"]))
		cerv2.append(cer2(ind["nw"],ind["sdchar"],ind["oov"],ind["lprob1"],ind["lprob2"]))
		cerv3.append(cer3(ind["nw"],ind["sdchar"],ind["oov"],ind["lprob1"],ind["lprob2"],ind["lprob3"]))
	df1=pd.DataFrame()
	df1["pass"]=dff["pass"]
	df1['length']  = df1['pass'].str.len()
	df1["GuessRank"]=dff["GuessRank"]
	df1["cer1"]=cerv1
	df1["cer2"]=cerv2
	df1["cer3"]=cerv3
	df1['1l']=df1['cer1']/df1['length']
	df1['2l']=df1['cer2']/df1['length']
	df1['3l']=df1['cer3']/df1['length']
	#print(df1.head(30))
	print(df1["cer2"].mean())
	#print(df1['cer1'].max(),df1['cer1'].min())
	print(df1['1l'].max(),df1['1l'].min())
	print(df1['2l'].max(),df1['2l'].min())
	print(df1['3l'].max(),df1['3l'].min())
	#df1.to_csv("./symspellres/heur0cer2noguess-top5p.csv",index=False)
	#df1.to_csv("./dicemarkovres/dice-top5p.csv",index=False)
	#df1.to_csv("./grseqres/cerbconst/comp-swD0-5del0-8cerorig.csv",index=False)
	#df1.to_csv("sw-all4.csv",index=False)
	#df1.to_csv("./trdoffcer/4word-60.csv",index=False)
	df1.to_csv("cer-mmap-dist.csv",index=False)
