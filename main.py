from load import loadpdf, loadfile
from search import results
from sys import setrecursionlimit, argv
import pickle

def main():
    setrecursionlimit(10000)
    if argv[2] == "0":
        data = loadpdf(argv[1] + ".pdf")
    elif argv[2] == "1":
        data = loadfile(argv[1] + ".pickle")
    query = str(input("Unesite reč, više reči ili frazu za pretragu: "))
    searchresults = results(data, query)
    print("\nRezultati pretrage:\n ")
    for i, result in enumerate(searchresults):
        if i > 0 and i % 10 == 0:
            ask = str(input("Unesite x da prekinete pretragu ili bilo koji drugi znak da nastavite: "))
            if ask == "x":
                break
        print("___________________________________________________________________\n")
        print(str(i + 1) + ". Stranica " + str(result.page.num))
        for find in result.index:
            queryresult = result.index[find]
            for queryindex in queryresult:
                if queryindex > 20 and queryindex < len(result.page.text) - len(find) - 20:
                    for i in range(queryindex - 20, queryindex + len(find) + 20):
                        print(result.page.text[i], end = "")
                elif queryindex < 20:
                    for i in range(0, queryindex + len(find) + 20):
                        print(result.page.text[i], end = "")
                else:
                    for i in range(queryindex - 20, len(result.page.text)):
                        print(result.page.text[i], end = "")
                print("\n")
    file = open(argv[1] + ".pickle", 'wb')
    pickle.dump(data, file)
    file.close()

if __name__ == "__main__":
    main()