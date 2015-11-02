#from HTMLParser import HTMLParser
#-*- coding: utf-8 -*-
import urllib.request,re,time

from html.parser import HTMLParser
from xml.etree import cElementTree as etree
from bs4 import BeautifulSoup



# create a subclass and override the handler methods

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tb = etree.TreeBuilder()
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        #print("\nData: "+self.get_starttag_text())
        if tag!='br':
            self.tb.start(tag, dict(attrs))
        
    def handle_startendtag(self, tag, attrs):
        #print("Encountered a startend tag:", tag)
        self.tb.start(tag, dict(attrs))
        self.tb.end(tag)
    def handle_endtag(self, tag):
        #print("Encountered an end tag:", tag)
        if tag!='br':
            self.tb.end(tag)
        
    def handle_data(self, data):
        #print("Encountered some data  :", data)
        self.tb.data(data)
    def close(self):
        HTMLParser.close(self)
        return self.tb.close()
        
        
# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
data = ''
f = urllib.request.urlopen('http://www.mobafire.com/league-of-legends/items')
data =f.read()
parser.feed(data.decode())
root = parser.close()
span = root.find(".//div[@id='browse-items']")
print("Adasdas: "+span.tag)

for child in span:
    itemparser=MyHTMLParser()
    #print(child.tag)
    #if child.attrib == 'class':
    #print( re.sub('[\s+]', ' ', child.attrib['class']))
    m = re.search('{(.+?)}', re.sub('[\s+]', ' ', child.attrib['class']))
    print(m.group(1))
    type=re.search('t:\'(.+?)\'', m.group(1))
    i=re.search('i:\'(.+?)\'', m.group(1))
    print(type.group(1)+'='+i.group(1))
    itemdata=''
    request = urllib.request.Request('http://www.mobafire.com/ajax/tooltip?relation_type='+type.group(1)+'&relation_id='+i.group(1))
    request.add_header("Content-Type","text/html;charset=utf-8")
    f=urllib.request.urlopen(request)
    itemdata=f.read().decode()
    #itemdata=itemdata.encode('ascii','ignore').decode()
    itemdata=itemdata.replace(u"\u2013", "-")
    #print('Data: '+itemdata)
    itemparser.feed(itemdata)
    parsed_html = BeautifulSoup(itemdata)
   
    txt=re.sub("[ ]+" , " ", parsed_html.find('div', attrs={'class':'item-info'}).get_text())
    txt=re.sub("[\n]{1,}" , "\n", txt)
    txt=re.sub("[\t]+" , "", txt)
    print("Text:\n"+txt)
    
    item=itemparser.close()
    print('root tag:'+item.tag)
    print('\n--------------------------------------------------------')
    #div=item.find(".//div[2]")
    #print("Div: "+div.text)
    

