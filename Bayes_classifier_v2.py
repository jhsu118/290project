import string
import json
from collections import *
import operator

##dropStopwords=FALSE

#import training and testing sets
'''with open('trainingset.json', 'rb') as fp:
    training = json.load(fp)
with open('testingset.json', 'rb') as fp:
    testing = json.load(fp)'''
with open('trainingset_reduced_over300.json', 'rb') as fp:
    training = json.load(fp)
with open('testingset_reduced_over300.json', 'rb') as fp:
    testing = json.load(fp)


##STRIP STOP WORDS
#if dropStopwords==TRUE:

f_stopwords = open('stopwords.txt','r')
stop_words = []
for line in f_stopwords:
    stop_words.append(line.strip())
stop_words = set(stop_words)
for course in testing:
    testing[course]["unique_words"]=[word for word in testing[course]["unique_words"] if word not in stop_words] #list comprehension, puts back in list only if not a stopword
for course in training:
    training[course]["unique_words"]=[word for word in training[course]["unique_words"] if word not in stop_words] #list comprehension, puts back in list only if not a stopword        
    
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

##CLASSIFIER BEGINS HERE
##return the number of classes in that department a word appears in
results={}
deptresults={}
progresscounter=0
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
                inflation += .00001
            probsnum.append(count)
        cleanprobs=[]
        for prob in probsnum: #inflate loop
            cleanprobs.append(float(prob+inflation)/(len(bydept_tr[dept])+inflation))
        alldeptprobs[dept]=reduce(mult, cleanprobs) * deptprob[dept]
    temp={} #dictionary to store results
    result = max(alldeptprobs.iteritems(), key=operator.itemgetter(1))[0]  ##add second /third 
    temp['result'] = result
    if testing[testcourse]['dept_code'] == result:
        temp['correct'] = True
    else:
        temp['correct'] = False
    temp['probs'] = alldeptprobs
    results[testcourse] = temp
    
    deptresults[progresscounter]={}    
    deptresults[progresscounter]['result']=temp['correct']
    deptresults[progresscounter]['dept_code']=testing[testcourse]['dept_code']
    deptresults[progresscounter]['testcourse']=testing[testcourse]['course_num']
    progresscounter+=1

##Evaluate how well our classifier did
numcorrect = 0
for key in results:
    if results[key]['correct']:
        numcorrect += 1

for key in results:
    print key, results[key]['result']


resultList=sorted(results.keys())
resultList2=[]
resultList3=[]
for testcourse in resultList:
    resultList2.append(results[testcourse]['result'])
    resultList3.append(results[testcourse]['correct'])
RESULT=zip (resultList, resultList2, resultList3)


Table2={}
for entry in deptresults.iteritems():
    if entry[1]['dept_code'] not in Table2:
        if entry[1]['result'] == True:
            Table2[entry[1]['dept_code']]={'Trues': 1, 'Falses': 0}
        if entry[1]['result'] == False:
            Table2[entry[1]['dept_code']]={'Trues': 0, 'Falses': 1}
       
        #{'falses': 0, 'trues':0}
    else:
        if entry[1]['result']==True:
            Table2[entry[1]['dept_code']]['Trues']+=1
        if entry[1]['result']==False:
            Table2[entry[1]['dept_code']]['Falses']+=1

FinalResult = {}
for entry in Table2:
    if entry not in numcourses2_tr.keys(): #There are six departments that are in testing set, but not in training set. Skip these.
        print entry
        continue
    FinalResult[entry] = [float(Table2[entry]['Trues'])/(Table2[entry]['Trues']+Table2[entry]['Falses']), Table2[entry]['Trues']+Table2[entry]['Falses'],numcourses2_tr[entry]]


