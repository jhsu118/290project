#build training model
import string

with open('trainingset.json', 'rb') as fp:
    training = json.load(fp)
with open('testingset.json', 'rb') as fp:
    testing = json.load(fp)

#adds a 'unique word' key that holds array of each class' unique words
globaluniquewords=[]
for key in training:
	description = str(training[key]['desc'])
	out=description.translate(string.maketrans("",""), string.punctuation)
	out=out.lower()
	array_of_words = out.split(' ')
	array_of_words=list(set(array_of_words))
	array_of_words.sort()
	training[key]['unique_words']=array_of_words
	globaluniquewords.extend(training[key]['unique_words'])	
globaluniquewords=list(set(globaluniquewords)) 
globaluniquewords.sort()   #global training set unique words

##repeat for testing set
testingsetuniquewords=[]
for key in testing:
	description = str(testing[key]['desc'])
	out=description.translate(string.maketrans("",""), string.punctuation)
	out=out.lower()
	array_of_words = out.split(' ')
	array_of_words=list(set(array_of_words))
	array_of_words.sort()
	testing[key]['unique_words']=array_of_words
	testingsetuniquewords.extend(testing[key]['unique_words'])	
testingsetuniquewords=list(set(testingsetuniquewords)) 
testingsetuniquewords.sort()   #global unique words


#courses in each department in the training set
numcourses={}
for key,value in training.iteritems():
	if value['dept_code'] not in numcourses:
		numcourses[value['dept_code']] = 1
		#print (key, value)
	else:
		numcourses[value['dept_code']] += 1
numcourses2={} #sorted version
for key in sorted(numcourses.iterkeys()):
	numcourses2[key]=numcourses[key]

# given a word, how many times does it appear in a department    
from collections import *

def findkeywordcount(word):
    keywordcount = defaultdict(int)
    for key in training:
        if word in training[key]['unique_words']:
            keywordcount[training[key]['dept_code']] += 1
    for key in training:
        if training[key]['dept_code'] not in keywordcount:
            keywordcount[training[key]['dept_code']] = 0
    return dict(keywordcount)

giantwordcount = {}
for word in globaluniquewords:
    giantwordcount[word] = findkeywordcount(word)

giantwordcount["workstations"]['RHETOR']/100

##NAIVE BAYESIAN CLASSIFIER

count = 0
specialwords = []
for course in testing:
    for word in testing[course]['unique_words']:
        if word not in giantwordcount:
            count += 1
            specialwords += [word]
bayes={} #dictionary of probabilities
for word in giantwordcount:
    temp = {}
    for dept in giantwordcount[word]:
        temp[dept] = float(giantwordcount[word][dept]) / (numcourses2[dept])
        #temp[dept] = float(giantwordcount[word][dept]+count) / (numcourses2[dept]+count) 
    bayes[word] = temp
#for word in specialwords:
#    temp = {}
#    for dept in numcourses2:
#        temp[dept] = 1.0 / (numcourses2[dept]+count)
#    bayes[word] = temp
   

deptprob = {}  #probability that a course belongs to a department just based on department sizes
for dept in numcourses2:
    deptprob[dept] = float(numcourses2[dept]) / len(training)


import operator
results = {}
for course in testing:
    probs = {}
    for dept in numcourses2:
        probs[dept] = deptprob[dept]
        #probs[dept] = math.log(deptprob[dept])
    for word in testing[course]['unique_words']:
        if word not in bayes: #this is to get rid of hebrewaramaric word
            continue       
        for dept in bayes[word]:
            probs[dept] *= bayes[word][dept]
            #probs[dept] += math.log(bayes[word][dept])
    temp = {}
    result = max(probs.iteritems(), key=operator.itemgetter(1))[0]
    temp['result'] = result
    if testing[course]['dept_code'] == result:
        temp['correct'] = True
    else:
        temp['correct'] = False
    temp['probs'] = probs
    results[course] = temp

numcorrect = 0
for key in results:
    if results[key]['correct']:
        numcorrect += 1

for key in results:
    print key, results[key]['result']

   