import  urllib.request
import re
import math
import matplotlib.pyplot as plt

# author = "Ian+Goodfellow"
author = input("Author name: ")
author = author.replace(' ','+')
# print(author)

url = "https://arxiv.org/search/?query=" + author + "&searchtype=author"
content = urllib.request.urlopen(url)
html_str = content.read().decode('utf-8')

# co_author_pattern = 'author&amp;query=[\s\S]*?</a>'
# co_author = re.findall(co_author_pattern,html_str)

page_pattern = 'of [0-9]* results for author:'
paper = re.findall(page_pattern, html_str)

paper_num = paper[0].split('of ')[1].split(" results")[0].strip()
#the result page number we want
page_num = math.ceil(int(paper_num)/50)
# print("Paper num : " + str(paper_num))
# print("Page num : " + str(page_num))
co_author_dict = {}
for i in range(0,int(page_num)):
    url = "https://arxiv.org/search/?query=" + author + "&searchtype=author&abstracts=show&size=50&order=-announced_date_first&start="+str(i*50)
    content = urllib.request.urlopen(url)
    html_str = content.read().decode('utf-8')
    # date_pattern = 'originally announced</span>[\s\S]*?</p>'
    # date = re.findall(date_pattern,html_str)
    co_author_pattern = 'author&amp;query=[\s\S]*?</a>'
    co_author = re.findall(co_author_pattern,html_str)
    for y in co_author:
        co_author_y = y.split(">")[1].split("<")[0].strip()
        if co_author_y in co_author_dict:
            co_author_dict[co_author_y] += 1
        else:
            co_author_dict[co_author_y] = 1
del co_author_dict[author.replace('+',' ')]

# print(sorted(co_author_dict))
for i in sorted(co_author_dict):
    print("[",i,"]",":",co_author_dict[i],"times")