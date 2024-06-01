import pypdf
from load import load

def main():
    data = load()
    query = str(input("Unesite reč, više reči ili frazu za pretragu: "))

if __name__ == "__main__":
    main()