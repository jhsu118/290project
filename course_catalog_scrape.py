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
		if url.attrs["href"][:22]=="http://general-catalog":  #filter out non-course catalog links
			good_urls.append(url.attrs["href"])
	except KeyError: #skips error
		continue
final_course_urls=[]
for url in good_urls:
	course_urls=[]
	html = urllib2.urlopen(str(url))
	soup=bs4.BeautifulSoup(html, "html5lib")
	#course_links=soup.find_all("a")#[2]
	print(url)
	for link in soup.find_all("a"):
		course_urls.append(link.get('href'))
	course_urls.pop(0) #remove first one, always useless
	for sub_url in course_urls:
		if sub_url[:18]=="gcc_list_crse_req?": #filter out non-coruse catalog
			final_course_urls.append(sub_url)
			print (sub_url)
final_course_urls=list(set(final_course_urls)) #drop duplicate department pages, down to 111
for i, p in enumerate(final_course_urls): #loop to add "http://... in front of each web address"
	final_course_urls[i]="http://general-catalog.berkeley.edu/catalog/"+p
	##FINALLY READY TO SCRAPE FROM THE PAGES OF INTEREST
for sub_url in final_course_urls:
	html = urllib2.urlopen(string(sub_url[0])
	soup=bs4.BeautifulSoup(html, "html5lib")
	bold_tags=soup.find_all("b")
	bold_tags.pop(0) #Drop first bold tag, which is not a course
#BUILD A DICTIONARY TO HOLD THE DATA
courses={}
counter=0
for iCourse in bold_tags:
	#number=re.findall('\d+\.','<B>[1-9]. class.')
	#m = re.match(r"\<b\>(\w+)\.(\s+)([\w\s]+)(.*)", "<b>11111AAA111111111111111111.  Military Physical Fitness and Nutrition. (1)  </b>")
	m = re.match(r"\<b\>(?P<number>\w+)\.(\s+)(?P<title>[\w\s]+)(.*)",  "<b>11111AAA111111111111111111.  Military Physical Fitness and Nutrition. (1)  </b>")
	m = re.match(r"\<b\>(?P<number>\w+)\.(\s+)(?P<title>[\w\s]+)(.*)",  iCourse.string.encode('ascii','ignore'))
	m = re.match(r"\<b\>(?P<number>\w+)\.(\s+)(?P<title>[\w\s]+)(.*)",'1. Military Physical Fitness and Nutrition. (1) ')  
	
	#m = re.match(r"\<b\>(?P<number>\w+)\.(\s+)(?P<title>[\w\s]+)(.*)", "<b>11111AAA111111111111111111.  Military Physical Fitness and Nutrition. (1)  </b>")      
	#print m.groups()
	courses[str(counter)] = {}
	courses[str(counter)] = m.groupdict()
	counter += 1

courses[str(counter)]['number'] = m.string[3]
    #courses[str(counter)]['title'] = title
    #courses[str(counter)]['dept_name_full'] = dept_name_full
    #courses[str(counter)]['dept_code'] = dept_code
    #[str(counter)]['desc'] = course_desc    
    counter += 1

	beautiful soup to get bold tags

#for sub_url in course_links:
	#try:
		#if# sub_url.attrs["href"][:73]=="http://general-catalog.berkeley.edu/catalog/gcc_list_crse_req?p_dept_name":  #filter out non-course catalog links
			#course_urls.append(url.attrs["href"])
#sub_url in course_links:
	#print(sub_url.get("href"))
	#course_urls.append(url.attrs["href"])
	#print url
	#good_urls.
	#soup.find_all('b')[2] #navigate the tree to grab the anchor tags below this b tag
	# then store each one in another variable called, e.g., dept_sub_urls = []
	
	#soup.find_all('b')[2].contents
	#str(soup.find_all('b')[2].contents[0])

	#next sibling, next element, children....
	#prettify

	#grab in bold, to first period.  periods in paren
	#end of course description (look for (F), (SP))#example regular expression to pull the course number. The first part is the expression and the second part will be whats in the tag..


