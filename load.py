import pypdf
from trie import Trie

class Page():
    def __init__(self, num, text, trie):
        self.num = num
        self.text = text
        self.trie = trie

def load():
    data = []
    reader = pypdf.PdfReader("tekst.pdf")
    for num, page in enumerate(reader.pages):
        trie = Trie()
        text = page.extract_text().split(" ")
        word = ""
        index = 0
        for i in len(text):
            letter = text[i]
            if letter in [",", ".", ":", ";", "-"]:
                continue
            elif letter == " ":
                trie.add(word, index) 
                index = i + 1
                word = ""  
            else:
                word += letter
        page = Page(num + 1, text, trie)
        data.append(page)
    return data