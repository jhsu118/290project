import urllib2
import bs4
import re
address="http://general-catalog.berkeley.edu/gc/curricula.html"
html = urllib2.urlopen(address)
#get links to department pages
soup = bs4.BeautifulSoup(html)
soup.title ##cool!
anchor_tags=soup.find_all("a")  #anchor tag catches all hyperlinks
good_urls=[]
for url in anchor_tags:
	try:
		if url.attrs["href"][:74]=="http://general-catalog.berkeley.edu/catalog/gcc_view_req?p_dept_cd=COM LIT":
			print "COM doublespace LIT will not be included" 
			continue
		if url.attrs["href"][:22]=="http://general-catalog":  #filter out non-course catalog links
			good_urls.append(url.attrs["href"])
	except KeyError: #skips error
		continue
final_course_urls=[]
for url in good_urls:
	course_urls=[]
	html = urllib2.urlopen(str(url))
	soup=bs4.BeautifulSoup(html, "html5lib")
	print(url)
	for link in soup.find_all("a"):
		course_urls.append(link.get('href'))
	course_urls.pop(0) #remove first one, always useless
	for sub_url in course_urls:
		if sub_url[:18]=="gcc_list_crse_req?": #filter out non-course catalog links
			final_course_urls.append(sub_url)
			print (sub_url)
final_course_urls=list(set(final_course_urls)) #drop duplicate department pages, down to 111
for i, p in enumerate(final_course_urls): #loop to add "http://... in front of each web address"
	final_course_urls[i]="http://general-catalog.berkeley.edu/catalog/"+p
##FINALLY READY TO SCRAPE FROM THE PAGES OF INTEREST
courses={} #BUILD A DICTIONARY TO HOLD THE DATA
counter=0
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
		if iCourse.string == None: #these courses have some bs4 string error 
			noStringCourses.append(iCourse)
		if iCourse.string!=None:  #issue: [<b>155.  Wonder and the Fantastic: <i>The Thousand and One Nights</i> in World Literary Imagination. (3)  </b>]
			m = re.match(r"(?P<number>\w+)\.(\s+)(?P<title>[\w\s]+)(.*)",  iCourse.string.encode('ascii','ignore'))
			dept_name_full=re.findall(r"\-\s(.*)\s+", soup.title.string.encode('ascii','ignore'))
			if m != None: 
				courses[str(counter)] = m.groupdict()
				courses[str(counter)]['dept_name_full'] = dept_name_full
				totalCourses += 1
				counter += 1
			if m == None: ## these crouses will not be matched wtih this regular expression. Need a hyphen int here somewhere.
				badCourses.append(iCourse)
#SCRAPING SUMMARY STATS
totalCoursesScraped = len(badCourses) + len(noStringCourses) + counter
print "Number of course websites visited %s" % len(final_course_urls)
print "Counter: %s" % counter  #7876 courses in dictionary
print "Regular expression will not much this number of courses: %s" % len(badCourses) #477
print "This number courses have some sort of bs4 string error: %s" % len(noStringCourses) #7
print "Total courses scraped, including un-dictionary-able ones: %s" % totalCoursesScraped  #8360

import json
with open('courses.json', 'wb') as fp:
    json.dump(courses, fp)

