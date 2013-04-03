import urllib2
import bs4

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

for url in good_urls:
	html = urllib2.urlopen(str(good_urls[0]))
	soup=bs4.BeautifulSoup(html, "html5lib")
	print url
	soup.find_all('b')[2] #navigate the tree to grab the anchor tags below this b tag
	# then store each one in another variable called, e.g., dept_sub_urls = []
	
	soup.find_all('b')[2].contents
	str(soup.find_all('b')[2].contents[0])

	next sibling, next element, children....
	prettify

	grab in bold, to first period.  periods in paren
	end of course description (look for (F), (SP))