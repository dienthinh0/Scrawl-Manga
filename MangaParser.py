from html.parser import HTMLParser
from enum import Enum

class WebName(Enum):
    MangaparkMe="mangapark.me"
    MangaparkCom="mangapark.com"
    batoto="bato.to"
    
def ExportImagesMPMe(datastr):
    parser = MangaParkMeParser()
    parser.feed(datastr)
    return parser

def ExportImagesMPCom(datastr):
    parser = MangaParkComParser()
    parser.feed(datastr)
    return parser

def ExportImagesBato(datastr):
    return None
    
def ExportImages(url, data):
    parser = None
    if WebName.MangaparkMe.value in url:
        parser = ExportImagesMPMe(data);
    elif WebName.MangaparkCom.value in url:
        parser = ExportImagesMPCom(data);
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
    def GetImages(self):
        return self.imagesUrl
    def GetName(self):
        return self.Name
    def PreProcessImageUrl(self,url):
        if 'http:' in url or 'https:' in url:
            return url
        return self.Prefix + url

class MangaParkMeParser(MangaParser):
    LogoUrl = "//static.mangapark.me/img/logo-mini.png"
    def __init__(self):
        MangaParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    if value != self.LogoUrl:
                        self.imagesUrl.append(self.PreProcessImageUrl(value))
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
        self.inLink = False
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    if value != self.LogoUrl:
                        self.imagesUrl.append(self.PreProcessImageUrl(value))
        if tag == 'title':
            self.inLink = True
            
    def handle_data(self, data):
        if self.inLink == True:
            self.inLink = False
            self.Name = self.ParseTitle(data)
            
    def ParseTitle(self,str):
        strs = str.split('ch.')
        return strs[0]+'ch.' + strs[1].split('-')[0].strip()
        
