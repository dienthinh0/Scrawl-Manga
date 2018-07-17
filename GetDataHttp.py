from enum import Enum
from html.parser import HTMLParser
from PIL import Image
from fpdf import FPDF
import Process
import urllib.request
import MangaParser
import io
import os
import shutil

Folder = "./Manga/"

class WebName(Enum):
    Mangapark="mangapark.me"
    bato="bato.to"

def Download(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    with urllib.request.urlopen(req) as f:
        data = f.read()
    return data

def ExportImagesMP(datastr):
    parser = MangaParser.MangaParkParser()
    parser.feed(datastr)
    return parser

def ExportImagesBato(datastr):
    return None
    
def GetDataImageStr(url):
    data = Download(url).decode('utf-8')
    imagesData= []
    parser  = None
    
    if WebName.Mangapark.value in url:
        parser = ExportImagesMP(data);
        
    elif WebName.bato.value in url:
        parser = ExportImagesBato(data);
        
    if parser is not None:
        imagesData.append(parser.GetName())
        imagesData.append(parser.GetImages())
    return imagesData

def DownloadAllImage(imagesUrl):
    FileImages = []
    progress =Process.Process()
    progress.setup(imagesUrl[0],len(imagesUrl[1])-1,CallbackDone)
    progress.start()
    for imageUrl in imagesUrl[1]:
        # UpdateUI
        FileImages.append(Download(imageUrl))
        progress.update()
        
    return FileImages
    
def createfolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating directory. ' +  dir)

def WritePDF(name,datas,outputDir):
    print("Writing")
    createfolder(outputDir)
    cover = Image.open(io.BytesIO(datas[0]))
    width, height = cover.size
    pdf = FPDF(unit = "pt", format = [width, height])
    i=0
    tempfolder = './temp/'
    createfolder(tempfolder)
    for data in datas:
        pdf.add_page()
        tempfile = tempfolder+"temp"+str(i)+".jpg"
        i=i+1
        with open(tempfile, 'wb') as file:
            file.write(data)
            file.close()
        pdf.image(tempfile, 0, 0)
        
    pdf.output(outputDir + name +".pdf", "F")
    shutil.rmtree(tempfolder)
    print("Writin Done")
    
def CallbackDone():
    print("Done")
    pass
    
def Parse(url):    
    data = GetDataImageStr(url)
    images = DownloadAllImage(data)
    WritePDF(data[0].strip(),images,Folder+data[0].strip()+"/")
    