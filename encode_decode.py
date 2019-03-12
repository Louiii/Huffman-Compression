import sys
import collections
import chardet
#import time
#from threading import Timer
#import timeit
#
#def print_time():
#    return time.time()

def encrypt(problem_file_name, write_name):
#    print('Encrypt')
#    curr_time = print_time()
    
    rawdata = open(problem_file_name, 'rb').read()
    result = chardet.detect(rawdata)
    charenc = result['encoding']
    
#    print('Binary read')
#    print(print_time()-curr_time)
#    curr_time = print_time()

    text_file = open(problem_file_name, 'r', encoding=charenc )
    
#    print('File opened')
#    print(print_time()-curr_time)
#    curr_time = print_time()
    
    character_list = []
    for line in text_file:
        for char in line:
            character_list.append(char)
    
 
    total_number_of_characters=len(character_list)
    counter = collections.Counter(character_list)
    
    values, counts = zip(*counter.most_common(total_number_of_characters)[::-1])#make to array of the values and the frequencies, uses [::-1] to reverse the order so that it is ascending
#print(counter)
    #DO A CHECK TO SEE IF VALUES IS LONG ENOUGH
    #branches = [(branch, sum), ... ]
    branches = [((values[0], values[1]) , counts[0] + counts[1])]
    values = values[2:]
    counts = counts[2:]
    
#    print('DONE COUNTER')
#    print(print_time()-curr_time)
#    curr_time = print_time()
    
    while(len(values) > 0):
        lowest_branch = min(branches, key = lambda t: t[1])
        #branch_value = lowest_branch[0]#this is the main section of the branch
        branch_count = lowest_branch[1]#this is the sum of the branch
        if (len(values) == 1 or counts[1] >= branch_count) :
            #if len(values) == 1, condition is satisfied, otherwise len(values) > 1 and therefore so is counts.
            #so then we also check if the second least frequent letter >= to the lowest branch
            #this essentially compares wether 1st + 2nd least frequent letter >= 1st least frequent letter + lowest branch
            #if it is, we must add the new letter to the branch
            branches.append(((lowest_branch, values[0]), counts[0] + branch_count))
            values = values[1:]#remove the letter we just added to the tree
            counts = counts[1:]
            branches.pop(branches.index(lowest_branch))#remove the branch we just added to.
        else :#in this case the 1st + 2nd least frequent letters is lower, so we do need a new branch
            branches.append((( values[0], values[1]), counts[0] + counts[1]))
            values = values[2:]
            counts = counts[2:]

    while(len(branches) > 1):#if there are multiple branches, group them by frequency as before
        lowest_branch = min(branches, key = lambda t: t[1])
        branches.pop(branches.index(lowest_branch))
        next_lowest_branch = min(branches, key = lambda t: t[1])
        branches.pop(branches.index(next_lowest_branch))
        branches.append(((lowest_branch, next_lowest_branch), lowest_branch[1] + next_lowest_branch[1]))
#    print('DONE TREE')
#    print(print_time()-curr_time)
#    curr_time = print_time()
        
#    print(branches)
    s_f = []#list that will contain the characters and their depths
    completed_routes = set()
    continu = True
    while (continu) :
        go_down = branches[0]
        string = ''
        while (True) :
            if (isinstance(go_down, str)) :#IF LEAF, ADD ROUTE AND BREAK
                #huffman.append( (go_down, string) )
                s_f.append((go_down, len(string)))
                completed_routes.add(string)
                break
            #CAN BE DUG DEEPER
            route = string

            if (len(go_down) == 0 or isinstance(go_down[1], int)): go_down = go_down[0]
            elif (isinstance(go_down[0], tuple) and isinstance(go_down[1], tuple)):

                if (route + '00') in completed_routes and (route + '01') in completed_routes:
                    go_down = go_down[1]
                    string += '1'
                else:
                    if route == '' or route + '0' not in completed_routes :
                        go_down = go_down[0]
                        string += '0'
                    elif (route + '1') not in completed_routes :
                        go_down = go_down[1]
                        string += '1'

            elif (isinstance(go_down[1], str)):
                if (route + '00') in completed_routes and (route + '01') in completed_routes:
                    go_down = go_down[1]
                    string += '1'
                else:
                    if (isinstance(go_down[0], tuple)):
                        if route == '' or route + '0' not in completed_routes :
                            go_down = go_down[0]
                            string += '0'
                    elif (isinstance(go_down[0], str)):
                        if (route + '0') not in completed_routes :
                            go_down = go_down[0]
                            string += '0'
                        elif (route + '1') not in completed_routes :
                            go_down = go_down[1]
                            string += '1'
        copy = set(completed_routes)
        for strg in copy:#For each route...
            if strg[-1] == '0':#If the route ends in a 0...
                first = strg[:-1]#make a variable that is the route, not including the last char.
                if (first + '1') in completed_routes or (first + '11') in completed_routes:
                    completed_routes.add(first)
        continu = False
        for char in string:
            if (char == '0') :
                continu = True
#    print('Done depths')
#    print(print_time()-curr_time)
#    curr_time = print_time()
                
    fre = list(set(list(map(lambda x:(x[1]),s_f))))[::-1]#makes a list of all the depths
    letters = []
    s_fr = []
    for f in fre:#puts all the characters at the same depth into: (list, depth) in a list for all depths, s_fr
        letters=[]
        for s in s_f:
            if s[1] == f:
                letters.append(s[0])
        s_fr.append((list(set(letters)), f))
    for _se in s_fr:
        _se[0].sort(key=lambda x:ord(x))#sort the characters at each depth alphabetically
    
    huffman = make_tree(s_fr)
#    print('Made canonical')
#    print(print_time()-curr_time)
#    print(print_time())
    writeHc(problem_file_name, write_name, character_list, huffman, s_fr, charenc)

def make_tree(sets_freqs):
    huffman = []
    codess = []
    next_route = ''
    for set_ in sets_freqs:#loop updating each route and assign the route to the characters Huffman code.
        next_route, codess = pass_set_return_closed_route(set_[0], set_[1], next_route)
        huffman += codess
    return huffman
#TAKE sets_freqs[0] (SET LIST) AND sets_freqs[1] (TREE LEVEL) AND MAKE TREE
    #this will be called when the hc file is written, and read

def front_concat0(total_length, end):
    while len(end) < total_length: end = '0' + end
    return end
def end_concat0(total_length, start):
    while len(start) < total_length: start += '0'
    return start
def remove_end0s(number):
    while number[-1] == '0': number = number[:-1]
    return number
def remove_ends(total_length, number):
    while len(number) != total_length: number = number[:-1]
    return number
def all_0s(length, next_route) :
    check = True
    for char in next_route:
        if char == '1':
            check = False
    if check:
        next_route = front_concat0(length, '1')
    if next_route[-1] == '0':
        next_route = next_route[:-1] + '1'
    return next_route
        

def to_binary(bina): 
    get_bin = lambda x: format(x, 'b')
    return get_bin(bina)

def pass_set_return_closed_route(chars, length, next_route) :
    codes = []
    num = 0
    if next_route != '':#make next route as a binary string the aprropriate length
        if len(next_route) > length:
            next_route = all_0s(length, remove_ends(length, next_route))#takes the (right end of the route off) and rebuilds the next route
        num = int(end_concat0(length, next_route), 2)#the integer value of the route
        
    for char in chars:#for each character at that depth increment num and turn it to binary
        codes.append((char, front_concat0(length, to_binary(num))))
        num += 1
    next_route = remove_end0s(front_concat0(length, to_binary(num)))
    return next_route, codes

def encode_header(encoding, s_freqs):
    max_level = s_freqs[0][1]
    s_freqs = s_freqs[::-1]
    binary = ''
    binary2= ''
    binary += front_concat0(8, to_binary(max_level))
    levels = []
    chars_on_level = []
    
    #print('Encoding check utf-8:')
    #print(s_freqs)
    #print(encoding)
    
    chars_set=[]
    for set_level in s_freqs:
        for char in set_level[0]:
            chars_set.append(char)
            
            
    for set_level in s_freqs:
        levels.append(set_level[1])
        chars_on_level.append(len(set_level[0]))
        
    #print(chars_on_level)
    if encoding == 'ascii':
        for ch in chars_set:
            binary2 += front_concat0(8, to_binary(ord(ch)))# + ' '
    elif encoding == 'utf-8':
        for ch in chars_set:
            binary2 += text_to_bits(ch)
    else:#elif encoding == 'UTF-16':
        for ch in chars_set:
            binary2 += text_to_bits(ch, encoding)
    #print(levels)
    
    #this writes the count for each level, in 1 bit, 2 bits etc.
    next_level = 0
    for level in range(1, max_level+1) :
        #writes 0 in binary form, only taking up less than the max bits required (equal to the level we're on)
        if level not in levels:
            binary += front_concat0(level, '0')
        else:#writes the number of characters on each successive level
            binary += front_concat0(level, to_binary(chars_on_level[next_level]))
            next_level += 1
    binary += binary2
    return binary
    
def writeHc(original_file_name, output_filename, character_list, huffman, s_freqs, encoding):
    if output_filename[-3:]=='.hc':
        output_filename = output_filename[:-3]
    
    binary_string = encode_header(encoding, s_freqs)
    #binary = ( [byte] ) , {bit}
    
    
    #first_3bits = remainder
    #+= encoding + '000'
    #+= noise_byte        <--- not there if remainder = 0
    #+= [max_level]{freq_on_level1}{{freq_on_level2}}{{{etc.}}}
    #+= [ascii value]...
    #+= main_string
    
    
    chars, binary = zip(*huffman[:])

    main_string = ''
    for character in character_list:
        main_string += binary[chars.index(character)]
    binary_string += main_string
        
    byte_array = []
    
    byte=''
    if encoding == 'utf-8' :
        enc = '00'
    elif encoding == 'ascii':
        enc = '01'
    else :
        enc = '10'
    remainder_of_bits = len(binary_string)%8#remainder of the byte that is noise
    
    if remainder_of_bits != 0 : 
        first_byte = front_concat0(3, to_binary(remainder_of_bits)) + enc + '000'
        noise_byte = front_concat0(8, binary_string[:remainder_of_bits])
        binary_string = binary_string[remainder_of_bits:]
        
        binary_string = first_byte + noise_byte + binary_string
        # make first byte of byte array a number indicating the number of bits to take off the last byte
    else:
        binary_string = '000' + enc + '000' + binary_string
      
    for i in range (len(binary_string)):#make binary string into a byte array
        if (i != 0 and i%8 == 0):
            byte_array.append(int(byte, 2))
            byte = ''
        byte += binary_string[i]
    byte_array.append(int(byte, 2))
    
            
    newFileByteArray = bytearray(byte_array)
    with open(output_filename + '.hc', 'wb') as file:#write
        file.write(newFileByteArray)
#    print('File written')
#    print(print_time())
        

def writeTxt(write_name, character_list, encd):
    if write_name[-4:]=='.txt':
        write_name = write_name[:-4]
    file = open(write_name + '.txt', 'w', encoding=encd )
    for character in character_list:
        file.write(str(character))
    file.close()
#    print('File written')
#    print(print_time())
    
def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def decrypt(readname, write_name):
#    print('Decrypt')
#    curr_time = print_time()
    
    binary_string = ''
    bin_array = []
    binary = ''
    with open(readname, "rb") as binary_file:
        data = binary_file.read()
        
#    print('Binary read')
#    print(print_time()-curr_time)
#    curr_time = print_time()
    
    for i in range(len(data)):
        binary = bin(bytes_to_int(data[i:i+1]))[2:]
        if (len(binary) < 8):
            for j in range(8 - len(binary)) :
                binary = '0' + binary
        bin_array.append(binary)
    for byt in bin_array:#remake binary string
        binary_string += byt
        
        
    #first_3bits = remainder
    #+= encoding + '000'
    #+= noise_byte        <--- not there if remainder = 0
    #+= [max_level]{freq_on_level1}{{freq_on_level2}}{{{etc.}}}
    #+= [ascii value]...
    #+= main_string
    
    remainder = int(binary_string[:3], 2)
    enc = binary_string[3:5]
    binary_string = binary_string[8:]

    if remainder != 0:
        binary_string = binary_string[8-remainder:]
    encoding = 'utf-8'
    if enc == '01':#find the encoding
        encoding = 'ascii'
    elif enc == '10':
        encoding = 'UTF-16'

    
    max_level = int(binary_string[:8], 2)#find the max level from where we encoded it to be
    binary_string = binary_string[8:]
    
    level_counts = []#find the number of characters on each level
    for level in range(1, max_level+1):
        level_counts.append(int(binary_string[:level], 2))
        binary_string = binary_string[level:]
    total_chars = sum(level_counts)#finds the total number of distinct characters
    
    
    chars = []
    bit_number = 8
    
    #utf-8:
    #if first bit of char code is 0 it is 1 byte
    #if first 2 bits of char code is 11 it is 2 bytes
    #if first 3 bits of char code is 111 it is 3 bytes
    #if first 4 bits of char code is 1111 it is 4 bytes
    #current_code = ''
    for i in range(total_chars):#decode all the characters in the header, put in chars list
        if encoding == 'utf-8':
            if binary_string[:2] == '11':
                bit_number = 16
                if binary_string[:4] == '1110': 
                    bit_number = 24
                if binary_string[:5] == '11110': 
                    bit_number = 32
            else : 
                bit_number = 8
            chars.append(bits_to_text(binary_string[:bit_number]))
        elif encoding == 'UTF-16' :
            bit_number = 16
            if binary_string[:2] == '11':
                bit_number = 32
            chars.append(bits_to_text(binary_string[:bit_number], encoding))
        else:
            chars.append(chr(int(binary_string[:bit_number], 2)))
        binary_string = binary_string[bit_number:]
    
    set_freqs = []
    current_level = 0
    current_set = []
    for freq in level_counts:#remake set_freqs
        current_level+=1
        if freq != 0:
            for i in range(freq):
                current_set.append(chars[0])
                chars.pop(0)
            set_freqs.append((current_set, current_level))
            current_set = []
    
    set_freqs = set_freqs[::-1]
    decoded_huffman = make_tree(set_freqs)#remake huffman

    
    chars, binary_codes = zip(*decoded_huffman[:])
#    print('huffman done')
#    print(print_time()-curr_time)
#    curr_time = print_time()
    
    bits = ''
    character_list = []#the remainder of the binary string is the huffman codes of the whole document
    for bit in binary_string:#as each bit is read, see if it is a character from the huffman we just decoded and add to a character list 
        bits += bit
        if bits in binary_codes:
            character_list.append(chars[binary_codes.index(bits)])
            bits = ''
#    print('main done')
#    print(print_time()-curr_time)
#    curr_time = print_time()
#    print(print_time())
    
    writeTxt(write_name, character_list, encoding)#the character list is all the text in the original document.


if len(sys.argv) == 4 :#requires 3 arguments, the file, and the name of the image to write and the name of what it should be writen as
    function_name = str(sys.argv[1])
    read_name = str(sys.argv[2])
    write_name = str(sys.argv[3])
    if function_name == 'encode':
        encrypt(read_name, write_name)
    if function_name == 'decode':
        decrypt(read_name, write_name)
    else:
        print ("incorrect arguments entered")
else:
    #print(timeit.timeit("encrypt('Input.txt', 'write_name')", setup="from __main__ import encrypt"))
    #print(timeit.timeit("decrypt('write_name.hc', 'write_name.txt')", setup="from __main__ import decrypt"))
    print ("incorrect number of arguments entered")
