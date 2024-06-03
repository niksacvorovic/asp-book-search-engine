from random import randint

class Result():
    def __init__(self, page, index, value):
        self.page = page
        self.index = index
        self.value = value

def results(data, query):
    resultlist = []
    querywords = query.split(" ")
    for page in data:
        index = {}
        value = 0
        for word in querywords:
            wordresult = page.trie.search(word)
            if wordresult == None:
                continue
            else:
                value += len(wordresult)
                index[word] = wordresult
        if index == {}:
            continue
        else:
            if len(index) > 1:
                value *= 2
            result = Result(page, index, value)
            resultlist.append(result)
    return sortresults(resultlist)

def sortresults(list):
    if len(list) == 0 or len(list) == 1:
        return list
    pivot = list[randint(0, len(list) - 1)]
    less = []
    more = []
    equal = [pivot]
    for elem in list:
        if pivot.value < elem.value:
            more.append(elem)
        elif pivot.value > elem.value:
            less.append(elem)
        else:
            equal.append(elem)
    sortedless = sortresults(less)
    sortedmore = sortresults(more)
    sorted = sortedmore + equal + sortedless
    return sorted
