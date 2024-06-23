import pypdf
import pymupdf
from trie import Trie
import pickle

class Page():
    def __init__(self, num, text, trie, refs):
        self.num = num
        self.text = text
        self.trie = trie
        self.refs = refs

def loadfile(filename):
    file = open(filename, 'rb')
    stream = pickle.load(file)
    file.close()
    return stream

def loadpdf(filename):
    data = []
    reader = pypdf.PdfReader(filename)
    firstpage = 0
    while reader.page_labels[firstpage] != '1':
        firstpage += 1
    for i in range(firstpage, reader.get_num_pages()):
        num = reader.page_labels[i]
        page = reader.pages[i]
        trie = Trie()
        text = page.extract_text().lower()
        word = ""
        index = 0
        for j in range(len(text)):
            letter = text[j]
            if letter in [",", ".", ":", ";", "-", "(", ")", " ", "\n"]:
                trie.add(word, index) 
                index = j + 1
                word = ""
            else:
                word += letter
        pagerefs = trie.search("page")
        if pagerefs == [] or pagerefs == None:
            page = Page(num, text, trie, [])
        else:
            refs = []
            for ref in pagerefs:
                pointer = ref + 5
                if not text[pointer].isnumeric():
                    continue
                pagenum = ""
                while text[pointer].isnumeric():
                    pagenum += text[pointer]
                    pointer += 1
                refs.append(int(pagenum) - 1)
            page = Page(num, text, trie, refs)
        data.append(page)
    return data

def save(searchresults):
    filename = str(input("Unesite x ako želite da završite izvršavanje programa ili unesite naziv pod kojim " +
                     "biste sačuvali fajl sa prvih 10 rezultata pretrage: "))
    if filename == "x":
        pass
    else:
        file = pymupdf.open()
        for i in range(10):
            if i >= len(searchresults):
                break
            page = file.new_page()
            pagetext = searchresults[i].page.text
            rectangle = pymupdf.Rect(50, 72, page.rect.width - 50, page.rect.height - 72)
            insert = page.insert_textbox(rectangle, pagetext, fontsize = 10)
        file.save(filename + ".pdf")