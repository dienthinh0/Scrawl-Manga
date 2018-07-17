from GetDataHttp import Parse
import sys
import os
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
    
if __name__ == "__main__":
    main(sys.argv[1:])