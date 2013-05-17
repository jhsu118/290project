''' Performs hierarchical agglomerative clustering on course descriptions.
1) Get course and description that goes with it and add to course list, removing stop words.
2) Calculate term frequency matrix using textmining python library
3) Generate linkage matrix Z
4) Generate hierarchical clusters
'''

import json
import numpy
import textmining
from scipy.spatial import distance
from scipy.cluster import hierarchy
import numpy as np

def termdocumentmatrix(courses):
    tdm = textmining.TermDocumentMatrix()
    for i in courses:
        tdm.add_doc(i)
    tdm.write_csv('course_matrix.csv', cutoff=2)

json_data=open('courses_data_set_upto300.json')

data = json.load(json_data)
courses = []
course_ids = {}  ## index of course ids for reference
index = 1

for i in data:
    courses.append(data[i]['desc'])
    course_ids[index] = {}
    course_ids[index]['title'] = data[i]['title']
    course_ids[index]['dept'] = data[i]['dept_code']
    course_ids[index]['code'] = i
    course_ids[index]['description'] = data[i]['desc']
    index += 1

'''Remove stop words'''
f_stopwords = open('stopwords.txt','r')
stop_words = []
for line in f_stopwords:
    stop_words.append(line.strip())

stop_words = set(stop_words)
f_stopwords.close()
 
all_courses = []

for descr in courses:
    new_description = ' '.join(word for word in descr.split() if word not in stop_words)
    course = new_description
    all_courses.append(course)
    
'''Computer term frequency matrix'''
result_tf = termdocumentmatrix(all_courses)

'''saving course matrix as a np array for quick access'''
feature_vectors = np.genfromtxt('course_matrix.csv', dtype =float, delimiter =',')
np.save('./features2.npy', feature_vectors)
feature_vectors = np.load('./features2.npy')
x = np.array(np.max(feature_vectors,axis=1), dtype=float)[:,np.newaxis]
feature_vectors = feature_vectors / x   ##normalizing term frequency matrix

'''Had an issue with -0 values so clipping values that are very small -0 and making them 0 so that clustering will not have errors'''
linkage = hierarchy.linkage(feature_vector[1::], method='complete', metric='cosine')    
np.clip(linkage, 0, np.amax(linkage), linkage)
np.save('./linkage.npy', linkage)
Z = np.load('./linkage.npy')

'''Generate clusters with linkage matrix Z, threshold = .9, and using the distance criteria'''
clusters = hierarchy.fcluster(Z, .9, criterion='distance') 
clusters_list = clusters.tolist()
print len(set(clusters_list))
print clusters_list
