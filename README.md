# generating-mempassphrase

#User passphrase generation

cd ~/passwords/probable-pp.txt - contains the 6.1M passwords before any filtering >=20 characters
cd ~/passwords/dict.txt - wiki corpus fed to symspell.py as dictionary. HERE change in paper, the frequencies are not set to 1.
cd ~/passwords/getpp.py - get passphrases with the proposed filtering and segmentation algorithms.
cd ~/passwords/symspell.py - further refine segmentation of obtained passphrases.


#Ngram Evaluation

cd ~/Ngram-Analytica/scrapengram.py - get ngram probability as json queries, input passphrases(works better)
cd ~/Ngram-Analytica/ngram.py - same but original code


#Wiki Data

Folder - /nobackup/avirup/wiki

gettagtext.py - gets title and body
pview.py - gets thepageview based on titles
title-pview.pkl contains sorted titles
Use wikiarticles.json after that to get the data respective to their titles. It has body and title. Process the body as per need.
Or use wikipedia package: https://github.com/goldsmith/Wikipedia to get the content based on titles directly {for current version} 


#MASCARA code

Folder - /nobackup/avirup/markov

ceroptgen.py the necessary pickles for bigrams, and length distribution are in same folder
dicegen.py for diceware generation. You can use length distribution or change percentile as you wish to.

*All combinations and modifications have been on ceroptgen.py, hence it might not be the current version.


#Evaluation

Guessability

~/ngeval/ {Pardon the name}
ppgenpp.py - to calculate the probabilities (input text file)
guess.py - convert probabilities to guess rank (input the previous generated probability pickle)
diceppguess.py - guess diceware passphrases based on its generation

CER

/nobackup/avirup/wiki
cer-5p.py - input the guessrank pickle file, get CER as csv


#Plots

Files added as pickles for both guessrank and CER

For guessrank:

Names user, dice mean as it is.
cerorig represents plain markov, while mmap and mascara are for the baselines.

mmap-dist is based on its own generation, with similar length distribution as user
mmap-mascara is the guessrank computed with the same model.

dice - diceware with markov based guess
dicen - using diceware implementation itself

For cer:

Names user, dice mean as it is.
cerorig represents plain markov, while mmap is the other baseline.

D0-xdel0-y represents mascara where D is the intermediate cer threshold of 0.x and bigram fraction of 0.y
