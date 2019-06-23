import  urllib.request
import re
import math
import matplotlib.pyplot as plt


# first, input the author name
# author = "Ian+Goodfellow"
author = input("Author name: ")
author = author.replace(' ','+')

#Sample code to get the html
url = "https://arxiv.org/search/?query=" + author + "&searchtype=author"
content = urllib.request.urlopen(url)
html_str = content.read().decode('utf-8')

# use regular expression to get paper num
page_pattern = 'of [0-9]* results for author:'
paper = re.findall(page_pattern, html_str)

# get the exact num of papers
paper_num = paper[0].split('of ')[1].split(" results")[0].strip()
page_num = math.ceil(int(paper_num)/50)
# print("Paper num : " + str(paper_num))
# print("Page num : " + str(page_num))

year_dict = {}
for i in range(0,int(page_num)):
    url = "https://arxiv.org/search/?query=" + author + "&searchtype=author&abstracts=show&size=50&order=-announced_date_first&start="+str(i*50)
    content = urllib.request.urlopen(url)
    html_str = content.read().decode('utf-8')
    date_pattern = 'originally announced</span>[\s\S]*?</p>'
    date = re.findall(date_pattern,html_str)
    for y in date:
        year = y.split("originally announced</span>")[1].split(".")[0].strip().split(" ")[1]
        if year in year_dict:
            year_dict[year] += 1
        else:
            year_dict[year] = 1
# year_dict = sorted(year_dict.items(),key=lambda d: d[0])
# print(year_dict.keys())
# # print(sorted(year_dict.keys()))
# print(year_dict.values())
pattern = 'title is-5 mathjax[\s\S]*?</p>'
result = re.findall(pattern , html_str)
# print("[Author: " + author + "]")

plt.bar(range(len(year_dict)), list(reversed(list(year_dict.values()))), align='center')
plt.xticks(range(len(year_dict)), list(reversed(list(year_dict.keys()))))
plt.show()