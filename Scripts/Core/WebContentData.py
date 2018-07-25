class WebContent:
    URL = ""
    Name = ""
    LinkImages = []
    DataImages = []
    def __init__(self):
        self.URL = ""
        self.Name = ""
        self.NumImages = 0
        self.LinkImages = []
        self.DataImages = []
        
    def ToString(self):
        return "(URL:" +self.URL + ") Name:" +self.Name +") (NumImages:" +self.NumImages+") Link:" +self.LinkImages