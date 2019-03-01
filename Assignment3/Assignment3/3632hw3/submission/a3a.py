import string
import sys


'''
1. Get the input; Done
   - def dataWord(dataList)

2. Find the length of the data word, parity bits and code word; Done
   - def calculateParityLength(dataWord)
   
3. Find the binary form of corresponding position numbers;
   - def positionNumberCalculator() 
     which calculates the position number according to the position in data word
     
4. Bit by bit XOR of binary forms of position numbers 
   whose corresponding data word bit is 1;
   
5. Output of the XOR result from the least significant to most significant bit.

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

def calculateParityLength(lenOfdataword):
    parityLength = 0
    toContinue = True
    while (toContinue):
        totalLen = parityLength + lenOfdataword
        if totalLen > 2**(parityLength - 1) and totalLen < 2**parityLength:
            toContinue = False
        else:
            parityLength = parityLength + 1

    return parityLength

def is_Power_of_Two(n):
    return n > 0 and (n & (n - 1)) == 0

def enlargeDataword(dataword, lenOfParity):
    enlargedDataword = [None] * (lenOfParity + len(dataword))
    # print("len of enlarged: ", len(enlargedDataword))
    i = 0
    for m in range(len(enlargedDataword)):
        if is_Power_of_Two(m+1):
            enlargedDataword[m] = None
        else:
            enlargedDataword[m] = dataword[i]
            i = i + 1
    
    return enlargedDataword

def bit_by_bit_XOR(listM, listN):
    
    listR = [None] * len(listM)
    
    for i in range(len(listM)):
        listR[i] = str(int(listM[i]) ^ int(listN[i]))
        
    return listR    

if __name__ == "__main__":
    
    dataString = sys.argv[1]
    
    dataList = list(dataString) # now we have the array of chars
    # print("dataList: ", dataList)
    
    dataword = dataWord(dataList, len(dataList))
    # print("dataword: ", dataword)
    
    lenOfParity = calculateParityLength(len(dataword))
    # print("lenOfParity: ", lenOfParity)
    
    enlargedDataword = enlargeDataword(dataword, lenOfParity)
    # print("enlarged dataword: ", enlargedDataword)
    
    
    list1 = [None] * lenOfParity
    
    for i in range(len(enlargedDataword)-1, -1, -1):
         
        if enlargedDataword[i] != '1':
            continue
        
        largestIndex = i
        list1 = int_to_bin_with_certain_length(largestIndex+1, lenOfParity)
        break
        
    for j in range(largestIndex-1, -1, -1):
        
        if enlargedDataword[j] != '1':
            continue
        
        list2 = int_to_bin_with_certain_length(j+1, lenOfParity)        
            
        list1 = bit_by_bit_XOR(list1, list2)
        
    listOfParity = list1
    
    # print("List of Parity: ", listOfParity)
    parity = ''.join(reversed(listOfParity))
    print(''.join(reversed(listOfParity)))
    
    # parity = ''
    # for i in range(lenOfParity-1, -1, -1):
    #     parity = parity + listOfParity[i]
    
    # print(parity)
    
    # print("backward: ")
    # for i in range(5, 0, -1):
    #     print(i)
    # result: 5 4 3 2 1
    
    
