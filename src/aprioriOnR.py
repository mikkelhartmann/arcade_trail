import numpy as np
import apriori
import ReccomenderSystem


R = np.load('R.npy')
R = np.array(R.tolist())

assosiationList = []

for ii in range(0,len(R)):
    assosiationList_temp = []
    for jj in range(0,len(np.transpose(R))):
        if R[ii,jj]==1:
         assosiationList_temp.append(str(jj+1))

    assosiationList.append(assosiationList_temp)

# Removing the empty lists (user IDs deleted)
for item in assosiationList:
    if item == []:
        assosiationList.remove(item)

# Doing the assosiation analysis
L,suppData = apriori.apriori(assosiationList,minSupport=0.10)
rules = apriori.generateRules(L,suppData,minConf=0.80)

# Loading the titles
titles = ReccomenderSystem.reading_titles('CSV/game_titles.csv')

# Pritty printing the assosiation rules
rule_string = []
for rule in rules:
    conf = round(rule[-1]*1000)/1000
    temp_title = []
    for frozen in rule[:-1]:
        for item in frozen:
            title = ReccomenderSystem.title_index_to_title(titles,str(item))
        temp_title.append(title)
    rule_string_temp = temp_title[0]+ ' implies '+ temp_title[1]+ ' with '+ str(conf) + ' confidence'
    rule_string.append(rule_string_temp)
print(rule_string)
