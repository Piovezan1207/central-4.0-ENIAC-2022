def binaryToInt( binaryList):
    val = 0

    val += binaryList[0] * 1
    val += binaryList[1] * 2
    val += binaryList[2] * 4
        
    return val


print(binaryToInt([1,0,0]))