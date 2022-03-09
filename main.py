from Huffman import HuffmanCoding
from Testo import Testo
def main():


    path = "textfile.txt"
    huffman = HuffmanCoding(path)
    exit = False


    while(not exit):
        choice = input("Enter 1 if you want to compress\nEnter 2 if you want to decompress \nenter 0 if you want to exit\n"  )
        if(choice == "1"):

            huffman.compress()

        if(choice == "2"):
            try:
                f = open('textfile_compressed.text', 'rb')
                f.close()
            except IOError:
                print('ERROR : File not found, Compress it first !\n')
                continue
            huffman.decompress("textfile_compressed.text")
        if  (choice=="0") :
             exit = True

if __name__ == '__main__':
    main()


