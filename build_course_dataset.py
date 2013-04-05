import re

courses = {}
f = open('coursecatalog.txt', 'r').read().replace('\n \n','__break__').replace('\n',' ').replace('__break__','\n__break__')
counter = 0

course_blocks = re.findall('__break__.*',f)

for entry in course_blocks[:-2]:

    title = re.findall('.*--\s\s',entry)[0].lstrip('__break__').rstrip('  --  ')  
    dept_name_full = re.findall('--.*?\s+\(',entry)[0].lstrip('--  ').rstrip('(').strip() 
    dept_code = re.findall('\s+\(.*?\)',entry)[0].lstrip(' (').rstrip(')').strip()
    course_desc = re.findall('Description.*\(', entry)[0][13:].rstrip('(').strip()

    courses[str(counter)] = {}
    courses[str(counter)]['title'] = title
    courses[str(counter)]['dept_name_full'] = dept_name_full
    courses[str(counter)]['dept_code'] = dept_code
    courses[str(counter)]['desc'] = course_desc
        
    counter += 1


for key, value in courses.iteritems() :
    print key, value


