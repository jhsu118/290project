import re
import json

courses = {}
f = open('coursecatalog.txt', 'r').read().replace('\n \n','__break__').replace('\n',' ').replace('__break__','\n__break__')
counter = 0

course_blocks = re.findall('__break__.*',f)

for entry in course_blocks:

    title = re.findall('.*--\s\s',entry)[0].lstrip('__break__').rstrip('  --  ')  
    dept_name_full = re.findall('--.*?\s+\(',entry)[0].lstrip('--  ').rstrip('(').strip() 
    
    flag = ')' in title
    
    if flag:
        dept_code = re.findall('\s+\(.*?\)',entry)[-1].strip().lstrip('(').rstrip(')')
        course_num = re.findall('\).*?\w+', entry)[-1].lstrip(') ')
    else:
        dept_code = re.findall('\s+\(.*?\)',entry)[0].lstrip(' (').rstrip(')').strip()
        course_num = re.findall('\).*?\w+', entry)[0].lstrip(') ')    
    
    if '(' in course_num:
        dept_code = re.findall('\s+\(.*?\)',entry)[1].strip().lstrip('(').rstrip(')')
        course_num = re.findall('\).*?\w+', entry)[1].lstrip(') ')
    
    course_desc = re.findall('Description.*\{', entry)[0][13:].rstrip(' {').strip()
        
    class_id = dept_code + ' ' + course_num
        
    if course_desc != '' and title != '' and class_id not in courses:
        courses[class_id] = {}
        courses[class_id]['title'] = title
        courses[class_id]['dept_name_full'] = dept_name_full
        courses[class_id]['dept_code'] = dept_code
        courses[class_id]['desc'] = course_desc    
'''       
for key, value in courses.iteritems():
	print key, value
'''

myfile = open('courses_data_set.json','w')
myfile.write(json.dumps(courses))


'''
Doc Stats:
10,373 courses originally.
No title: 443
No dept name full: 0
No dept code: 0
No description: 897
9466 courses with title, dept, and description.
5777 unique courses
'''
