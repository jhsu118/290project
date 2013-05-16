##Builds a data and test set
import json
import random
import math
import string

with open('courses_data_set.json', 'rb') as fp:
    data = json.load(fp)

#adds a 'unique word' key that holds array of each class' unique words
globaluniquewords=[]
for key in data:
	description = str(data[key]['desc'])
	out=description.translate(string.maketrans("",""), string.punctuation)
	out=out.lower()
	array_of_words = out.split(' ')
	array_of_words=list(set(array_of_words))
	array_of_words.sort()
	data[key]['unique_words']=array_of_words
	globaluniquewords.extend(data[key]['unique_words'])	
globaluniquewords=list(set(globaluniquewords)) 
globaluniquewords.sort()   #global data set unique words

#new dictionary in the {dept: classes}, format
bydept={}
for course in data.iteritems():
	dept_code=course[1]['dept_code']
	if dept_code not in bydept.keys():
		bydept[str(dept_code)]=[course[0]]
	else:
		bydept[str(dept_code)].append(course[0])

#select testing set: 10% of each department
testingcourses=[]
for dept in bydept:
	testingcourses.extend(random.sample(bydept[dept],int(math.ceil(.1*len(bydept[dept]))))) #adding list to another list

testing={}
for course in testingcourses:
	testing[course]=data[course]

training = {}##this is our training set!!!!!
for course in data:
    if course not in testingcourses:
        training[course] = data[course]
    else:
        print "did not add course"

with open('dataset_with_word_arrays.json', 'wb') as fp:
    json.dump(data, fp)
with open('testingset.json', 'wb') as fp:
    json.dump(testing, fp)
with open('trainingset.json', 'wb') as fp:
    json.dump(training, fp)


