import sys
sys.path.insert(0, sys.path[0]+'\\Core')
import os
from GetDataHttp import GetDataImageStr, DownloadAllImage, WritePDF
import WebContentData
import Process


Folder = "./Manga/"
def ReadFile(fileDir):
    with open(fileDir,"r") as file:
        pages = []
        while True:
            page =file.readline()
            if page is "":
                break
            pages.append(page)
        file.close()
        return pages
    return None

def main(argv):
    if len(argv) != 1:
        print("Missing parmeter")
        exit()
    if ".txt" in argv[0]:
        if os.path.exists(argv[0]):
            listpage = ReadFile(argv[0])
            if listpage is not None:
                for page in listpage:
                    Parse(page)
            else:
                print("File struct wrong")
        else:
            print("File not exist")
            exit()
    else:
        Parse(argv[0])

def OnUpdate():
    pass
        
def Parse(url):
    content = WebContentData.WebContent()
    content.URL = url
    fetchdata = GetDataImageStr(url)
    if fetchdata is None:
        print ("Wrong URL")
        exit()
    content.Name,content.LinkImages = fetchdata
    
    progress =Process.Process()
    progress.setup(content.Name,len(content.LinkImages))
    progress.start()
    content.DataImages = DownloadAllImage(content.LinkImages,lambda:progress.update())
    progress.finish()
    print ("Done")
    WritePDF(content.Name.strip(),content.DataImages,Folder+content.Name.strip()+"/")

    
if __name__ == "__main__":
    main(sys.argv[1:])