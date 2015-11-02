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
f = urllib.request.urlopen('http://www.mobafire.com/league-of-legends/item/trinity-force-63')
data =f.read()
parser.feed(data.decode())
root = parser.close()

span = root.findall(".//td[@class='recipe-bar']")

#print("Adasdas: "+span[0].tag)
for tr in span:
    for child in tr:
        print(child.tag)
        for childchild in child:
            print('  '+childchild.tag)
            for img in childchild:
                print('    '+img.attrib['src'])
                m = re.search('{(.+?)}', re.sub('[\s+]', ' ', img.attrib['class']))
                print(m.group(1))
                type=re.search('t:\'(.+?)\'', m.group(1))
                i=re.search('i:\'(.+?)\'', m.group(1))
                print(type.group(1)+'='+i.group(1))
