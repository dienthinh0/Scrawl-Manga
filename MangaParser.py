from html.parser import HTMLParser

class MangaParkParser(HTMLParser):
    LogoUrl = "//static.mangapark.me/img/logo-mini.png"
    Prefix ="http:"
    imagesUrl =[]
    Name = None
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
    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    if value != self.LogoUrl:
                        self.imagesUrl.append(self.Prefix + value)
                if name == 'title':
                    if self.Name is None:
                        self.Name = value[:-7]
    def GetImages(self):
        return self.imagesUrl
    def GetName(self):
        return self.Name
