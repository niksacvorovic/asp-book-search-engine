import pypdf
from trie import Trie
import pickle

class Page():
    def __init__(self, num, raw, text, trie, refs):
        self.num = num
        self.raw = raw
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
        raw = reader.pages[i]
        trie = Trie()
        text = raw.extract_text().lower()
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