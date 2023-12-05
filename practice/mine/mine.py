from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import re
import scrapy
html = urlopen('https://pythonscraping.com/pages/page1.html')
# print(html.read())
print('\n')
'''
这段代码是使用Python的urllib库中的urlopen函数打开一个网页，并打印出该网页的内容。
但是，这段代码存在一个问题，即在第一次调用html.read()后，文件指针已经移动到了文件的末尾，所以在第二次调用html.read()时，它将返回空字符串。
如果你想再次读取网页内容，你需要重新打开文件或者将文件指针重置到文件的开头。
'''
# print(html.read())
bs = BeautifulSoup(html.read(), 'lxml')
print(bs.h1)
bs.findAll()
bs.find_all()
re.compile()