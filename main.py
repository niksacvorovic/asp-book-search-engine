from load import loadpdf, loadfile
from search import results
from queryfunctions import autocomplete, autocorrect
from sys import setrecursionlimit, argv
import pickle

def printchar(j, queryindex, find, result):
    if j == queryindex:
        print("\x1b[6;33;40m", end = "")
    if j == queryindex + len(find):
        print("\x1b[0m", end = "")
    symbol = result.page.text[j]
    print(symbol, end = "")


def main():
    setrecursionlimit(10000)
    if argv[2] == "0":
        data = loadpdf(argv[1] + ".pdf")
    elif argv[2] == "1":
        data = loadfile(argv[1] + ".pickle")
    # data = loadfile("knjiga.pickle")
    query = str(input("Unesite reč, više reči ili frazu za pretragu: "))
    if " " not in query and query[-1] == "*":
        completions = autocomplete(data, query)
        if completions == []:
            print("Nije pronađena reč sa datim početkom")
        else:
            print("Pronađene su sledeće reči za dati upit: ")
            for i, word in enumerate(completions):
                print(str(i + 1) + ") " + word)
            while True:
                choose = str(input("Odaberite jednu od ponuđenih reči ili unesite x da prekinete pretragu: "))
                if choose == "x":
                    print("___________________________KRAJ PRETRAGE_________________________________")
                    file = open(argv[1] + ".pickle", 'wb')
                    pickle.dump(data, file)
                    file.close()
                    exit()
                else:
                    try:
                        arrayindex = int(choose) - 1
                        if arrayindex > 0 and arrayindex <= len(completions):
                            query = completions[arrayindex]
                            break
                        else:
                            print("Neispravan unos! Pokušajte opet")
                    except:
                        print("Neispravan unos! Pokušajte opet")
    searchresults = results(data, query)
    if len(searchresults) < 2:
        corrections = autocorrect(data, query)
        if corrections != []:
            print("Da li ste hteli da pretražite: ")
            for i, word in enumerate(corrections):
                print(str(i + 1) + ") " + word)
            while True:
                choose = str(input("Odaberite jednu od ponuđenih reči ili unesite x ako ipak želite da pretražite prvobitnu reč: "))
                if choose == "x":
                    break
                else:
                    try:
                        arrayindex = int(choose) - 1
                        if arrayindex >= 0 and arrayindex <= len(corrections):
                            query = corrections[arrayindex]
                            searchresults = results(data, query)
                            break
                        else:
                            print("Neispravan unos! Pokušajte opet")
                    except:
                        print("Neispravan unos! Pokušajte opet")
    if searchresults == []:
        print("Za datu pretragu nema rezultata!")
    else:
        print("\nRezultati pretrage:\n ")
        i = 0
        while i < len(searchresults):
            result = searchresults[i]
            if i > 0 and i % 10 == 0:
                while True:
                    print("Za prelazak na sledeću stranu pretrage unesite znak >")
                    print("Za povratak na prethodnu stranu pretrage unesite znak <")
                    print("Za prekid pretrage unesite x")
                    ask = str(input("Odaberite opciju: "))
                    if ask == ">":
                        break
                    elif ask == "<":
                        if i >= 20:
                            i -= 20
                            break
                        else:
                            print("Ovo je prva stranica! Unesite neku drugu opciju")
                    elif ask == "x":
                        print("___________________________KRAJ PRETRAGE_________________________________")
                        file = open(argv[1] + ".pickle", 'wb')
                        pickle.dump(data, file)
                        file.close()
                        exit()
                    else:
                        print("Uneli ste nepostojeću opciju. Pokušajte opet")
            print("___________________________________________________________________\n")
            print(str(i + 1) + ". Stranica " + result.page.num)
            for find in result.index:
                queryresult = result.index[find]
                for queryindex in queryresult:
                    if queryindex > 30 and queryindex < len(result.page.text) - len(find) - 30:
                        for j in range(queryindex - 30, queryindex + len(find) + 30):
                            printchar(j, queryindex, find, result)
                    elif queryindex < 30:
                        for j in range(0, queryindex + len(find) + 30):
                            printchar(j, queryindex, find, result)
                    else:
                        for j in range(queryindex - 30, len(result.page.text)):
                            printchar(j, queryindex, find, result)
                    print("\n")
            i += 1
        print("___________________________KRAJ PRETRAGE_________________________________")
    file = open(argv[1] + ".pickle", 'wb')
    pickle.dump(data, file)
    file.close()

if __name__ == "__main__":
    main()