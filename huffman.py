class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __lt__(self, other):
        return (comes_before(self,other))


def comes_before(a, b):
    if a.freq<b.freq:
        return True
    elif a.freq==b.freq:
        if a.char<b.char:
            return True
        return False
    return False

def combine(a, b):
    if a.char<b.char:
        new_node=HuffmanNode(a.char,a.freq+b.freq)
        new_node.set_left(a)
        new_node.set_right(b)
        # new_node.left=a
        # new_node.right=b
        return new_node
    elif b.char<a.char:
        new_node=HuffmanNode(b.char,a.freq+b.freq)
        new_node.set_left(a)
        new_node.set_right(b)
        # new_node.left=a
        # new_node.right=b
        return new_node

def cnt_freq(filename):
    try:
        file=open(filename,'r')
    except:
        raise(FileNotFoundError)
    freqlist=[0]*256
    for character in file.read():
        ASCII=ord(character)
        freqlist[ASCII]+=1
    if max(freqlist)==0:
        file.close()
        return None
    file.close()
    return (freqlist)



def create_huff_tree(char_freq):
    node_list=[]
    ASCII=0
    #creates the list of node ------ chr(0)->chr(256) if exist
    for freq in char_freq:
        if freq>0:
            new_node=HuffmanNode(ASCII,freq)
            node_list.append(new_node)
        ASCII += 1
    #print(node_list)
    node_list.sort()
    #print(node_list)
    while len(node_list)>1:
        combined_node=combine(node_list[0],node_list[1])
        del node_list[0]
        del node_list[0]
        node_list.append(combined_node)
        node_list.sort()
    root=node_list[0]
    return root




def create_code(node):
    code_list=['']*256
    if node.left is not None:
        code="0"
        create_code_helper(node.left,code_list,code)
    if node.right is not None:
        code="1"
        create_code_helper(node.right,code_list,code)
    return code_list

def create_code_helper(node,list,code):
    if node.left is None and node.right is None:
        list[node.char]=code
    if node.left is not None:
        create_code_helper(node.left,list,code+'0')
    if node.right is not None:
        create_code_helper(node.right,list,code+'1')



def create_header(freqs):
    header=""
    ASCII=0
    for frequency in freqs:
        if frequency>0:
            header+=str(ASCII)+" "+str(frequency)+" "
        ASCII+=1
    new=header.strip()
    return new



def huffman_encode(in_file, out_file):
    create_file=open(out_file,'w')
    frequency_list=cnt_freq(in_file)
    if frequency_list==None:
        create_file.close()
        return
    #HuffmanTree=create_huff_tree(frequency_list)
    #code_list=create_code(HuffmanTree)
    code_list=create_code(create_huff_tree(frequency_list))
    header = create_header(frequency_list)

    file=open(in_file,'r')
    code01=""
    for characters in file.read():
        # for index in range(len(code_list)):
        #     if ord(characters)==index and code_list[index]!=None:
        #         code01+=code_list[index]
        if code_list[ord(characters)] != '':
            code01 += code_list[ord(characters)]

    if code01=="":
        filetext=header
        create_file.write(filetext)
        file.close()
        create_file.close()
    else:
        filetext=header+"\n"+code01
        create_file.write(filetext)
        file.close()
        create_file.close()


def huffman_decode(encoded_file, decode_file):
    try:
        in_file=open(encoded_file,'r')
    except:
        raise(FileNotFoundError)
    out_file=open(decode_file,'w')

    header=in_file.readline()
    encoded_text = in_file.read()
    decoded_text = ''
    frequency_list=parse_header(header)

    if encoded_text=='' and max(frequency_list)!=0:
        temp=header.split()
        letter=chr(int(temp[0]))*int(temp[1])
        decoded_text+=letter
        out_file.write(decoded_text)
        in_file.close()
        out_file.close()
        return

    if max(frequency_list)==0:
        in_file.close()
        out_file.close()
        return
    HuffmanTree=create_huff_tree(frequency_list)
    HuffmanTree2=HuffmanTree

    for num in encoded_text:
        if num == '0':
            HuffmanTree2=HuffmanTree2.left
        elif num == '1':
            HuffmanTree2=HuffmanTree2.right
        if HuffmanTree2.left == None and HuffmanTree2.right == None:
            decoded_text+=chr(HuffmanTree2.char)
            HuffmanTree2=HuffmanTree

    in_file.close()
    out_file.write(decoded_text)
    out_file.close()

def parse_header(header_string):
    freq_list=[0]*256
    header=header_string.split()
    for index in range(0,len(header),2):
        ASCII=int(header[index])
        frequency=int(header[index+1])
        freq_list[ASCII]=frequency
    return freq_list


#print(create_code(create_huff_tree([1]*256)))



# temp=[0]*96
# temp.append(5)
# temp.append(6)
# temp.append(5)
# print(create_huff_tree(temp))
# print(create_header(temp))
# print(create_code(create_huff_tree(temp)))
#huffman_encode("God's Plan Lyrics.txt","God's Plan Lyrics_Out.txt")
#huffman_encode("6a.txt","6a_Out.txt")
# huffman_encode("declaration.txt","declaration_out.txt")
#huffman_encode("allchar.txt","allchar_out.txt")
# huffman_decode("declaration_out.txt","test.txt")

# def filecreate():
#     file=open('allchar.txt','w')
#     chars=''
#     for i in range(128):
#         ascii=chr(i)
#         chars+=ascii
#     file.write(chars)
#     file.close()
# filecreate()
