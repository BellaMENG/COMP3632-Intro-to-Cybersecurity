import sys

'''
1. Convert the second argument (data) to list of bits;

2. Find the correct/incorrect codeword;

3. Find position numbers of elements which are 1;

4. XOR the position numbers found;

5. If the result of XOR is 0, then correct;
   else, the decimal form of the result of XOR is the position number
   of the incorrect bit;
   
6. If the position number is power of 2, then the parity is incorrect;
   else, the data word is incorrect;
   
7. Find the correct parity or data word.

'''

def dataWord(dataList, length):
    # returns a list of bits in char type
    datawordString = ""
    asciiList = [None] * length
    i = 0
    for ele in dataList:
        asciiList[i] = int(ord(ele))
        i = i + 1
    
    for ele in asciiList:
        datawordString = datawordString + '{0:08b}'.format(ele)
        
    dataword = list(datawordString)
    return dataword

def is_Power_of_Two(n):
    return n > 0 and (n & (n - 1)) == 0

def int_to_bin_with_certain_length(inputInt, length):
        
    bitString = '{0:b}'.format(inputInt)
    diff = length - len(bitString)
    
    if diff > 0:
        zeros = ''
        for i in range(diff):
            zeros = zeros + '0'
        
        bitString = zeros + bitString
        
    ReturnList = list(bitString)
    
    return ReturnList

def bit_by_bit_XOR(listM, listN):
    
    listR = [None] * len(listM)
    
    for i in range(len(listM)):
        listR[i] = str(int(listM[i]) ^ int(listN[i]))
        
    return listR   

def list_to_str(list2):
    str_of_bits = ''
    for i in range(len(list2)):
        str_of_bits = str_of_bits + list2[i]
    
    return str_of_bits

def list_of_bits_to_str(list1):
    
    str_of_bits = list_to_str(list1)
    asc = int(str_of_bits, 2)
    character = chr(asc)
    return character




if __name__ == "__main__":
    
    parity_stream = sys.argv[1]
    data = sys.argv[2]
    
    parity = list(parity_stream)
    datalist = list(data)

    dataword = dataWord(datalist, len(datalist))
    # print("dataword: ", dataword)

    len_of_codeword = len(parity) + len(dataword)
    # print(len_of_codeword)

    codeword = [None] * len_of_codeword
    # print("parity: ", parity)

    index_of_parity = 0
    index_of_dataword = 0
    for i in range(len_of_codeword):
        if is_Power_of_Two(i+1):
            codeword[i] = parity[index_of_parity]
            index_of_parity = index_of_parity + 1
            
        else:
            codeword[i] = dataword[index_of_dataword]
            index_of_dataword = index_of_dataword + 1

    # print("codeword: ", codeword)

    resultList = [None] * len(parity)

    for i in range(len_of_codeword-1, -1, -1):
        if codeword[i] == '1':
            largest_index = i
            break

    resultList = int_to_bin_with_certain_length(largest_index+1, len(parity))

    for j in range(largest_index-1, -1, -1):
        if codeword[j] != '1':
            continue
        list2 = int_to_bin_with_certain_length(j+1, len(parity))
        
        resultList = bit_by_bit_XOR(resultList, list2)
        
    # print("result list: ", resultList)

    correct = True
    for i in range(len(resultList)):
        if resultList[i] == '1':
            correct = False
            break

    if not correct:

        errorcode = ''
        for i in range(len(parity)):
            errorcode = errorcode + resultList[i]
            
        position_number = int(errorcode, 2)
        # print(position_number)
        
        if codeword[position_number-1] == '0':
            codeword[position_number-1] = '1'
        else:
            codeword[position_number-1] = '0'
            
        # print("corrected codeword: ", codeword)
        
        new_parity = parity
        m = 0
        new_dataword = dataword
        n = 0
        
        for i in range(len_of_codeword):
            if is_Power_of_Two(i+1):
                new_parity[m] = codeword[i]
                m = m + 1
            else:
                new_dataword[n] = codeword[i]
                n = n + 1
            
        # print("new parity: ", new_parity)
        # print("new dataword: ", new_dataword)
        
        parity = new_parity
        dataword = new_dataword
        
        new_parity = list_to_str(new_parity)
        # print("new parity: ", new_parity)
        
        parity_stream = new_parity
        
        num_of_char = int(len(dataword)/8)
        # print("num of char: ", num_of_char)
        
        new_data = ''
        
        for i in range(num_of_char):
            char = list_of_bits_to_str(dataword[i*8:i*8+8])
            new_data = new_data + char
        
        # print("new data: ", new_data)
        
        data = new_data

    print(parity_stream)
    print(data)

