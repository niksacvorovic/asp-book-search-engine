from load import loadpdf, loadfile
from search import results, autocomplete
from sys import setrecursionlimit, argv
import pickle

def main():
    setrecursionlimit(10000)
    if argv[2] == "0":
        data = loadpdf(argv[1] + ".pdf")
    elif argv[2] == "1":
        data = loadfile(argv[1] + ".pickle")
    data = loadfile("knjiga.pickle")
    query = str(input("Unesite reč, više reči ili frazu za pretragu: "))
    if " " not in query and query[-1] == "*":
        autocomplete(query)
    searchresults = results(data, query)
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
                            print(result.page.text[j], end = "")
                    elif queryindex < 30:
                        for j in range(0, queryindex + len(find) + 30):
                            print(result.page.text[j], end = "")
                    else:
                        for j in range(queryindex - 30, len(result.page.text)):
                            print(result.page.text[j], end = "")
                    print("\n")
            i += 1
        print("___________________________KRAJ PRETRAGE_________________________________")
    file = open(argv[1] + ".pickle", 'wb')
    pickle.dump(data, file)
    file.close()

if __name__ == "__main__":
    main()