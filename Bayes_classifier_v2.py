import string
import json
from collections import *
import operator

#import training and testing sets
with open('trainingset.json', 'rb') as fp:
    training = json.load(fp)
with open('testingset.json', 'rb') as fp:
    testing = json.load(fp)

##PREPARE DICTIONARIES AND FUNCTIONS FOR CLASSIFIER TO USE

#Function for classifier to multiply all conditional probabilities
def mult(x,y):
	return x*y

#new dictionary from training set in the {dept: classes}, format
bydept_tr={}
for course in training.iteritems():
	dept_code=course[1]['dept_code']
	if dept_code not in bydept_tr.keys():
		bydept_tr[str(dept_code)]=[course[0]]
	else:
		bydept_tr[str(dept_code)].append(course[0])

#new dictionary for 
numcourses_tr={}
for key,value in training.iteritems():
	if value['dept_code'] not in numcourses_tr:
		numcourses_tr[value['dept_code']] = 1
		#print (key, value)
	else:
		numcourses_tr[value['dept_code']] += 1
numcourses2_tr={} #sorted version
for key in sorted(numcourses_tr.iterkeys()):
	numcourses2_tr[key]=numcourses_tr[key]

#probability that a course belongs to a department just based on department sizes
deptprob = {}  
for dept in numcourses2_tr:
    deptprob[dept] = float(numcourses2_tr[dept]) / len(training)

##Create a list of unique words in the training set
trainingunique=[]
for array in training:
	trainingunique.extend(training[array]['unique_words'])	
trainingunique=list(set(trainingunique)) 
trainingunique.sort()  

#Conditional probabilities: given a word, in how many course descriptions does it appear in a department?    
def findkeywordcount(word):
    keywordcount = defaultdict(int)
    for dept in bydept_tr:
    	for course in bydept_tr[dept]:
    		if word in training[course]['unique_words']:
        		keywordcount[dept] += 1
    return dict(keywordcount)
deptwordcount = {}
for word in trainingunique:
    deptwordcount[word] = findkeywordcount(word)

##return the number of classes in that department a word appears in
results={}
progresscounter=0
##CLASSIFIER
for testcourse in testing:
    print progresscounter
    alldeptprobs={}
    for dept in bydept_tr.keys(): 
        probsnum=[]
        inflation=0
        for word in testing[testcourse]["unique_words"]:   
            if word not in trainingunique:
                continue
            #find the count and append it to probsnum
            try:
                count = deptwordcount[word][dept]
            except:
                count = 0
            #if len(deptwordcount[word].keys()) == 1:
               # count = 1000
            if count == 0:
                inflation += .0001
            probsnum.append(count)
        cleanprobs=[]
        for prob in probsnum: #inflate loop
            cleanprobs.append(float(prob+inflation)/(len(bydept_tr[dept])+inflation))
        alldeptprobs[dept]=reduce(mult, cleanprobs) * deptprob[dept]
    temp={} #dictionary to store results
    result = max(alldeptprobs.iteritems(), key=operator.itemgetter(1))[0]
    temp['result'] = result
    if testing[testcourse]['dept_code'] == result:
        temp['correct'] = True
    else:
        temp['correct'] = False
    temp['probs'] = alldeptprobs
    results[testcourse] = temp
    progresscounter+=1

##Evaluate how well our classifier did
numcorrect = 0
for key in results:
    if results[key]['correct']:
        numcorrect += 1

for key in results:
    print key, results[key]['result']

resultsordered=results.sort


"""
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
for word in trainignuniquewords:
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
    print key, results[key]['result'] """