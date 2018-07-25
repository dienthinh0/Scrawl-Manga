from html.parser import HTMLParser
from PIL import Image
from fpdf import FPDF
import urllib.request
import MangaParser
import io
import os
import shutil


def Download(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    with urllib.request.urlopen(req) as f:
        data = f.read()
    return data

def GetDataImageStr(url):
    data = Download(url).decode('utf-8')
    imagesData= []
    parser  = MangaParser.ExportImages(url,data)
    if parser is not None:
        imagesData.append(parser.GetName())
        imagesData.append(parser.GetImages())
    else:
        return None
    return imagesData

def DownloadAllImage(imagesUrl, callback = None):
    FileImages = []
    for imageUrl in imagesUrl:
        FileImages.append([Download(imageUrl),imageUrl.split('.')[-1:][0]])
        callback()
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
    # find best size
    wh = []
    width=0
    height = 0
    for data in datas:
        cover = Image.open(io.BytesIO(data[0]))
        w, h = cover.size
        if w in wh:
            width = w
            height= h
            break
        else:
            wh.append(w)
    pdf = FPDF(unit = "pt", format = [width, height])
    i=0
    tempfolder = './temp/'
    createfolder(tempfolder)
    # Start add images
    for data in datas:
        pdf.add_page()
        i=i+1
        tempfile = tempfolder+"temp"+str(i)+"."+data[1]
        with open(tempfile, 'wb') as file:
            file.write(data[0])
            file.close()
        #make center image and scale
        cover = Image.open(io.BytesIO(data[0]))
        w, h = cover.size
        scalew = 1.0 if w<=width else 1.0*w/width
        scaleh = 1.0 if h<=height else 1.0*h/height
        scaleratio = scalew if scalew>scaleh else scaleh
        pdf.image(tempfile,0 if width<=(w/scaleratio) else (width-w/scaleratio)/2,0 if height<=(h/scaleratio) else (height-h/scaleratio)/2,w/scaleratio ,h/scaleratio)
    pdf.output(outputDir + name +".pdf", "F")
    shutil.rmtree(tempfolder)
    print("Writing Done")
    
def DebugData(str):
    with open("webhtml.txt","w",encoding= "utf-8") as f:
        f.write(str)
        f.close
