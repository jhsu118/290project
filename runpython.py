course_urls=[]
course_links=soup.find_all("a")#[2]
for link in soup.find_all('a'):
		course_urls.append(link.get('href'))
course_urls.pop(0)
final_course_urls=[]
for sub_url in course_urls:
	if sub_url[:30]=="gcc_list_crse_req?p_dept_name=": 
		final_course_urls.append(sub_url)
		
