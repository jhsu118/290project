import json
import pprint
import re
import string
import matplotlib.pyplot as plt

with open('courses_data_set.json', 'rb') as fp:
    data = json.load(fp)

pprint.pprint(data.keys())
lengths = []
all_words=[]
for course in data.iteritems():
    description = str(course[1]['desc'])
    array_of_words = description.split(' ')
    num_of_words = len(array_of_words)
    lengths.append(num_of_words)
    all_words.extend(array_of_words)
all_words_clean=[] #strip punctuation
for word in all_words:
	s = word
	clean=s.translate(string.maketrans("",""), string.punctuation)
	all_words_clean.append(clean)

#avg_words = sum(len)/len(lengths) #mean
print "before deduped"
deduped=[] #array of unique words across all course descriptions
for word in all_words_clean:
	if str(word) not in deduped:
		deduped.append(word)	
		print word
print "done deduping"		
deduped=[x.lower() for x in deduped] #make everything lower case

wordcount={}
for word in deduped:  #counting instances of each word
	count = all_words_clean.count(word)
	wordcount[word]=count

grammarWords=["a","as","the", "will", "or","that","their", "be", "also", "have", "about", "above", "across", "after", "against", "along", 
"among", "around", "at", "before", "behind", "below", "beneath", "beside" ,"between", 
"beyond" ,"but" ,"by", "despite", "down" ,"during", "except", "for", "from", "in" ,"inside", "into", 
"like", "near" ,"of" ,"off" ,"on", "onto", "out" ,"outside", "over", "past" ,"since", "through",
 "throughout", "till", "to", "toward", "under", "underneath", "until", "up", "upon,", "with", "within", "without"]
 schoolWords=["course", "students", "topics",""]

temp=wordcount
plt.hist
plt.hist(wordcount.values(),bins=50)# wordcount.keys())

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)

ordered=sorted(wordcount, key=wordcount.get, reverse=True)[1:len(wordcount)]

for w in sorted(wordcount, key=wordcount.get, reverse=True):
  print w, wordcount[w]
  ordered.append

"""



len(str(data["YIDDISH 101"]["desc"]).split #prints length of description

for course in data.iteritems:
	description=str(course[1]['desc']).split
	print description

len(str.split

Histogram: number of words, mean/m/m
Histogram: common words (top 100)

Histogram: number of courses in departments, mean/m/m
Stats: # cross listed courses

Histogram and table: Number of unique words/department"""