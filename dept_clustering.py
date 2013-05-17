'''Performs hierarchical agglomerative clustering for departments
1) Get department and description that goes with it and add description to that departments list
2) Calculate similarity between pairs of departments
3) Generate linkage matrix and dendrogram
4) Print cluster list
'''
import json
import numpy
import textmining
from scipy.spatial import distance
from scipy.cluster import hierarchy
from matplotlib.pyplot import show

def termdocumentmatrix(depts, dept_ids):
    tdm = textmining.TermDocumentMatrix()
    for key in dept_ids.keys():
        tdm.add_doc(depts[dept_ids[key]])
    return tdm.rows(cutoff=2)

json_data=open('courses_data_set_upto300.json')
data = json.load(json_data)

depts = {}

for i in data:
    if data[i]['dept_code'] not in depts:
        depts[data[i]['dept_code']]= data[i]['desc']
    else:
        depts[data[i]['dept_code']] += ' ' + data[i]['desc']

dept_ids = {}    #dictionary to keep track of department order
index = 1
for key in depts:
    dept_ids[index] = key
    index += 1

'''Compute term frequency matrix for departments'''
result_tf = termdocumentmatrix(depts, dept_ids)

feature_vector = []
for row in result_tf:
    feature_vector.append(row)

'''Department labels for dendrogram'''
dept_labels = ['HMEDSCI','JOURN','ENGIN','ESPM','ASAMST','ECON','EPS','VIS STD','DUTCH','THAI','SEASIAN','HISTART','FILM','DEMOG','CHINESE','CLASSIC','PHYS ED','PERSIAN','PSYCH','COG SCI','UGBA','EA LANG','SCANDIN','JAPAN','CELTIC','MED ST','SOC WEL','ASIANST','GPP','IAS','BIOLOGY','PACS','SANSKR','UGIS','CIV ENG','COM LIT','STAT','IND ENG','HIN-URD','FRENCH','COLWRIT','GSPDP','AFRICAM','ETH GRP','SEMITIC','CHM ENG','KHMER','CHEM','MFE','ENVECON','PUB POL','NATAMST','DEVP','YIDDISH','OPTOM','LINGUIS','EAEURST','PUNJABI','LGBT','ASTRON','PORTUG','EL ENG','LD ARCH','BIO ENG','EWMBA','ETH STD','INTEGBI','PHILOS','AMERSTD','TAGALG','VIS SCI','SLAVIC','ILA','JEWISH','MALAY/I','NUC ENG','GWS','EDUC','PHYSICS','ISF','LATAMST','MEC ENG','LATIN','M E STU','MIL SCI','PLANTBI','BANGLA','LNS','MEDIAST','SPANISH','EURA ST','KOREAN','GERMAN','PB HLTH','COMPSCI','FILIPN','GMS','SOCIOL','AEROSPC','INFO','XMBA','S ASIAN','ENV SCI','A,RESEC','TIBETAN','ENV DES','NE STUD','LEGALST','MIL AFF','ENGLISH','GREEK','LAN PRO','NWMEDIA','ARCH','ITALIAN','CMPBIO','VIETNMS','ANTHRO','NAV SCI','CHICANO','MBA','BUDDSTD','NUSCTX','S,SEASN','TAMIL','GEOG','THEATER','CY PLAN','RHETOR','MAT SCI','DEV STD','ENE,RES','MUSIC','PHDBA','CRIT TH','POL SCI','ARABIC','HISTORY','ART','MCELLBI','SCMATHE','RELIGST','POLECON','MATH']


'''Compute linkage matrix and generate dendrogram'''
linkage = hierarchy.linkage(feature_vector[1::], method='complete', metric='cosine')    
dendrogram = hierarchy.dendrogram(linkage, labels=dept_labels, leaf_font_size=8)
show()

'''Prints hierachical clusters'''
clusters = hierarchy.fclusterdata(feature_vector[1::], .1, criterion='distance', method='complete', metric='cosine')
clusters_list = clusters.tolist()
print clusters_list
