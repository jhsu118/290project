courses={} #BUILD A DICTIONARY TO HOLD THE DATA
counter=0
badCourseCounter = 0
badCourses=[]
noStringCourses=[]
totalCourses=0
for sub_url in final_course_urls:
	html = urllib2.urlopen(str(sub_url))
	print str(sub_url)
	soup=bs4.BeautifulSoup(html, "html5lib")
	bold_tags=soup.find_all("b")
	bold_tags.pop(0) #Drop first bold tag, which is not a course
	for iCourse in bold_tags:
		if iCourse.string == None:
			noStringCourses.append(iCourse)
		if iCourse.string!=None:  #issue: [<b>155.  Wonder and the Fantastic: <i>The Thousand and One Nights</i> in World Literary Imagination. (3)  </b>]
			m = re.match(r"(?P<number>\w+)\.(\s+)(?P<title>[\w\s]+)(.*)",  iCourse.string.encode('ascii','ignore'))
			dept_name_full=re.findall(r"\-\s(.*)\s+", soup.title.string.encode('ascii','ignore'))
			if m != None: 
				courses[str(counter)] = m.groupdict()
				courses[str(counter)]['dept_name_full'] = dept_name_full
				totalCourses += 1
				counter += 1
			if m == None: ## this course creates proble
				badCourses.append(iCourse)
				badCourseCounter += 1
