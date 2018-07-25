from html.parser import HTMLParser
from enum import Enum

class WebName(Enum):
    MangaparkMe="mangapark.me"
    MangaparkCom="mangapark.com"
    MangadexOrg="mangadex.org"
    batoto="bato.to"
    
def ExportImagesMPMe(datastr):
    parser = MangaParkMeParser()
    parser.feed(datastr)
    return parser

def ExportImagesMPCom(datastr):
    parser = MangaParkComParser()
    parser.feed(datastr)
    return parser
    
def ExportImagesMangadex(datastr):
    parser = MangadexOrgParser()
    parser.feed(datastr)
    return parser

def ExportImagesBato(datastr):
    parser = BatotoParser()
    parser.feed(datastr)
    return parser
    
def ExportImages(url, data):
    parser = None
    if WebName.MangaparkMe.value in url:
        parser = ExportImagesMPMe(data);
    elif WebName.MangaparkCom.value in url:
        parser = ExportImagesMPCom(data);
    elif WebName.MangadexOrg.value in url:
        parser = ExportImagesMangadex(data);
    elif WebName.batoto.value in url:
        parser = ExportImagesBato(data);
    return parser

    
class MangaParser(HTMLParser):
    imagesUrl = []
    Name = None 
    Prefix ="http:"
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.dataArray = []
        self.countLanguages = 0
        self.lasttag = None
        self.lastname = None
        self.lastvalue = None
        self.imagesUrl = []
        self.Name = None
    def feed(self, data):
        HTMLParser.feed(self,data)
    def GetImages(self):
        return self.imagesUrl
    def GetName(self):
        return self.Name
    def PreProcessImageUrl(self,url):
        extention = url.split('.')[1]
        finalurl = url
        if 'http:' in url or 'https:' in url:
            finalurl =  url
        else:
            finalurl = self.Prefix + url
        self.imagesUrl.append(finalurl)

class MangaParkMeParser(MangaParser):
    LogoUrl = "//static.mangapark.me/img/logo-mini.png"
    def __init__(self):
        MangaParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    if value != self.LogoUrl:
                        self.ProcessImageUrl(value)
        if tag == 'title':
            self.inLink = True

    def ParseTitle(self,str):
        strs = str.split('ch.')
        return strs[0]+'ch.' + strs[1].split('-')[0].strip()

    def handle_data(self, data):
        if self.inLink == True:
            self.inLink = False
            self.Name = self.ParseTitle(data)

class MangaParkComParser(MangaParser):
    LogoUrl = "//static.mangapark.com/img/logo-mini.png"
   
    def __init__(self):
        MangaParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    if value != self.LogoUrl:
                        self.PreProcessImageUrl(value)
        if tag == 'title':
            self.inLink = True
            
    def handle_data(self, data):
        if self.inLink == True:
            self.inLink = False
            self.Name = self.ParseTitle(data)
            
    def ParseTitle(self,str):
        strs = str.split('ch.')
        return strs[0]+'ch.' + strs[1].split('-')[0].strip()

class MangadexOrgParser(MangaParser):
    def __init__(self):
        MangaParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.inLink = True
            
    def handle_data(self, data):
        if self.inLink == True:
            self.inLink = False
            self.Name = self.ParseTitle(data)
            
    def ParseTitle(self,str):
        strs = str.split(')')
        strtitle = strs[0].split('(')
        return strtitle[1]+' ' + strtitle[0].strip()
        
    def feed(self,str):
        MangaParser.feed(self,str)
        self.ParseImages(str)
    def ParseImages(self,str):
        PrefixURL = 'https://mangadex.org'
        server = str.split("var server = '")[1].split("';")[0]
        dataurl = str.split("var dataurl = '")[1].split("';")[0]
        pages = str.split('var page_array = [')[1].split(']')[0].replace("'","").split(',')
        for page in pages:
            if page is not None and page is not "":
                self.PreProcessImageUrl(PrefixURL+server+dataurl+'/'+page.split()[0])

class BatotoParser(MangaParser):
    LogoUrl = "//static.bato.to/img/manga/batoto-logo-2.png?v1"
   
    def __init__(self):
        MangaParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.inLink = True
            
    def handle_data(self, data):
        if self.inLink == True:
            self.inLink = False
            self.Name = data
    def feed(self,str):
        MangaParser.feed(self,str)
        self.ParseImages(str)
    def ParseImages(self,str):
        pages = str.split("var images = {")[1].split("};")[0].replace('"','').split(',')
        for page in pages:
            if page is not None and page is not "":
                self.PreProcessImageUrl(page.split(':',1)[1])

