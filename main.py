from load import load
from search import results

def main():
    data = load()
    query = str(input("Unesite reč, više reči ili frazu za pretragu: "))
    searchresults = results(data, query)
    print("\nRezultati pretrage:\n ")
    for result in searchresults:
        print("___________________________________________________________________")
        print("Stranica " + str(result.page.num))
        for find in result.index:
            if find > 20 and result.index[0] < len(result.page.text) - len(query) - 20:
                for i in range(find - 20, find + len(query) + 20):
                    print(result.page.text[i], end = "")
            elif find < 20:
                for i in range(0, find + len(query) + 20):
                    print(result.page.text[i], end = "")
            else:
                for i in range(find - 20, len(result.page.text)):
                    print(result.page.text[i], end = "")
            print("\n")

if __name__ == "__main__":
    main()