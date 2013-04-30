##Builds a training set
import json
import random
import math


with open('courses_data_set.json', 'rb') as fp:
    data = json.load(fp)

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
	#testing.pop(course)

training = {}##this is our training set!!!!!
for course in data:
    if course not in testingcourses:
        training[course] = data[course]
    else:
        print "did not add course"

with open('trainingset.json', 'wb') as fp:
    json.dump(training, fp)
with open('testingset.json', 'wb') as fp:
    json.dump(testing, fp)


