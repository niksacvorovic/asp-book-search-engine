from random import randint

class Result():
    def __init__(self, page, index, value):
        self.page = page
        self.index = index
        self.value = value

def results(data, query):
    resultlist = []
    for page in data:
        index = page.trie.search(query)
        if index == None:
            continue
        else:
            value = len(index)
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
    sorted = sortedless + equal + sortedmore
    return sorted
