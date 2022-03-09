import heapq
import os
import math
import time
from Node import Node



class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # functions for compression:

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in text:
                frequency[character]=0
            frequency[character] = frequency.get(character, 0) + 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = Node(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while (len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1 #smallest
            merged.right = node2 #2nd smallest

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, current_node, current_code):
        if (current_node == None):
            return

        if (current_node.char != None):
            self.codes[current_node.char] = current_code
            self.reverse_mapping[current_code]=current_node.char
            return

        self.make_codes_helper(current_node.left, current_code + "0")
        self.make_codes_helper(current_node.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):

        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"         #put zeros at the end of the text to make it divisible by 8

        padded_info = "{0:08b}".format(extra_padding)   #put at the beginning of the text the value of the added padding in a binary form(1 byte)
        encoded_text = padded_info + encoded_text
        return encoded_text
    def pad_encoded_char_code(self,code):
        extra_padding=0

        numOfBytesDecimal=math.ceil(len(code)/8)
        numOfbytes = "{0:04b}".format(numOfBytesDecimal)
        if len(code)%8==0:
            extra_padding=0
        else:
            extra_padding =  (8*numOfBytesDecimal)- len(code) % (8*numOfBytesDecimal)
            for i in range(extra_padding):
                code="0"+code

        padded_info = "{0:04b}".format(extra_padding)
        encoded_code = numOfbytes+padded_info + code

        return encoded_code
    def get_byte_array(self, padded_encoded_text):
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def pad_char(self, encoded_char):
        if len(encoded_char)==8:
            return encoded_char
        extra_padding = 8 - len(encoded_char) % 8

        for i in range(extra_padding):
            encoded_char = "0" + encoded_char

        return encoded_char

    def write_char_bytes_number(self):
        number_of_character_bytes = len(self.codes)
        number_of_character_bytes = format(number_of_character_bytes, 'b')
        number_of_character_bytes = self.pad_char(number_of_character_bytes)

        return number_of_character_bytes
    def write_char_bytes(self):
        padded_encoded_chars=""
        for char, code in self.codes.items():
            char = ord(char)  # get ascii code
            encoded_char = format(char, 'b')  # ascii to binary
            encoded_char = self.pad_char(encoded_char)
            code = str(code)
            padded_code = self.pad_encoded_char_code(code)  # padding of code added to code
            padded_encoded_char = padded_code + encoded_char  # contains padded_code + binary character ( 1bytes +1 bytes), padding info not included

            padded_encoded_chars+=padded_encoded_char
        return padded_encoded_chars



    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename+"_compressed"+ ".text"
        mappingcode=""

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            size_before_comp = "textfile.txt"

            file_stats_before = os.stat(size_before_comp)
            start = time.time()
            text = file.read()
            text = text.rstrip()
            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            mappingcode+=self.write_char_bytes_number()
            mappingcode+=self.write_char_bytes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)
            mappingcode+=padded_encoded_text
            b = self.get_byte_array(mappingcode)

            output.write(bytes(b))
            end = time.time()
        print("Compressed")
        size_after_comp = "textfile_compressed.text"

        file_stats_after = os.stat(size_after_comp)
        ratio = ((file_stats_after.st_size) / (file_stats_before.st_size))
        x = round(ratio,3)
        print(f'File Size after compression is {file_stats_after.st_size} Bytes or {round((file_stats_after.st_size / (1024 * 1024)),4)} Mega Bytes')
        print(f'ratio between the file size after to before compression {x} ')
        print(f"Time taken to compress the file {round((end - start),3)} secs")
        return output_path

    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text
    def remove_padding_char_code(self,padded_encoded_code):
        padded_info = padded_encoded_code[0:4]        #padded_encode_code contains padded_info from bits[0:3] and the rest is the padded code
        extra_padding = int(padded_info, 2)
        padded_encoded_code = padded_encoded_code[4:]
        encoded_code = padded_encoded_code[extra_padding:]
        return encoded_code


    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if (current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text
    def decode_characters(self,input,initial_elements_number):

        identifier=1 #=1: padding, =2:code, =3:character
        map={}
        padding=""
        encoded_code=""
        numOfBytes=1
        for i in range(initial_elements_number):
            byte=input.read(1)
            byte = ord(byte)                    #hexa to decimal
            bits = bin(byte)[2:].rjust(8, '0')  #decimal to binary string

            if identifier==1:
                numOfBytes=int(bits[0:4],2)
                padding=bits[4:8]

            if identifier==2:
                code=bits
                for j in range(numOfBytes-1): #loop to read more bytes if the code is more than one byte
                    byte = input.read(1)
                    byte = ord(byte)  # hexa to decimal
                    bits = bin(byte)[2:].rjust(8, '0')  # decimal to binary string
                    code=code+bits

                encoded_code = padding + code

                encoded_code = self.remove_padding_char_code(encoded_code)
                padding=""
                numOfBytes=1
            if identifier==3:
                decimal_char = int(bits, 2)  # decimal value of char( from binary to ascii)
                char = chr(decimal_char)  # from decimal(ascii) to char
                map[encoded_code] = char
                encoded_code=""
                identifier = 0


            identifier+=1

        return map
    def decompress(self, input_path):

        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"
        #self.reverse_mapping = x.encode()

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            # reading count of characters
            start = time.time()
            number_of_characters = file.read(1)
            number_of_characters = ord(number_of_characters) # Hexa to decimal
            initial_elements_number = number_of_characters * 3 # number of characters (2,3,4_byte code + 1_byte character) we are setting the initial value (2_bytes for code and 1_byte character
            # reading characters

            self.reverse_mapping=self.decode_characters(file,initial_elements_number)

            #reading text
            bit_string = ""
            byte=file.read(1)   # ebd2 mn el byte ele b3dhom 3oltol
            while (len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)
            output.write(decompressed_text)
            end = time.time()
        print("Decompressed")
        print(f"Time taken to decompress the file {round((end - start), 3)} secs")

        return output_path
