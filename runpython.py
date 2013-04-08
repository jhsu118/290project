courses={}
counter=0
for iCourse in bold_tags:
	number=re.findall(, <b>124AB. Classname. )
	courses[str(counter)] = {}
	courses[str(counter)]['number'] = number
	counter += 1

m=re.match(r"\w+",str(bold_tags[4]))
print m.groups()