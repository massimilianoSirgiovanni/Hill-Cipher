import math as mt

m = 0


def getKey():
    # GET KEY FROM USER
    key = input("Insert the Key: ")

    return list(key)


def verifyKey(key):
    # VERIFY IF THE KEY IS INVERTIBLE
    det = detMatrix(key) % 26
    if det == 0 or mt.gcd(det, 26) != 1:
        print("KEY NOT USABLE!")
        return 0
    else:
        return 1


def setKey():
    # GET KEY AND VERIFY IF IT IS USABLE, RETURN THE KEY IN BLOCKS
    while True:
        key = getKey()
        if len(key) / m != m:
            print("NOT SQUARE KEY!")
            print("TRY ANOTHER KEY")
        elif len(key) < 2:
            print("THE KEY IS TOO SHORT")
            print("TRY ANOTHER KEY")
        else:
            blockKey = textInBlocks(key)
            if verifyKey(blockKey) == 1:
                return blockKey
            else:
                print("TRY ANOTHER KEY")


def readFile(fileName):
    # READ A TEXT FROM A FILE
    file = open(fileName, "r")
    words = file.read().splitlines()  # puts the file into an array
    file.close()
    return list(words[0])


def saveText(text, fileName):
    # WRITE A TEXT IN A FILE
    textStr = "".join(text)
    file = open(fileName, "w")
    file.write(textStr)  # puts the file into an array
    file.close()
    print(f"SAVED TEXT IN {fileName}")


def textInBlocks(text):
    # TRANSFORM THE TEXT IN A LIST OF BLOCKS
    blocks = []
    tmp = []
    j = 0
    for i in range(0, len(text)):
        # CONSTRUCTION OF BLOCKS OF LENGTH m
        if j == m:
            # FULL BLOCK IS INSERTED IN THE LIST
            blocks.append(tmp)
            tmp = []
            j = 0

        tmp.append(ord(text[i]) - 65)
        j = j + 1

    # VERIFY IF THE LAST BLOCK IS FULL
    if len(tmp) == 0:
        # IF THE LAST BLOCK IS EMPTY
        return blocks
    elif len(tmp) < m:
        # IF THE LAST BLOCK IS NOT EMPTY BUT IS NOT FULL
        for i in range(len(tmp), m):
            tmp.append(-1)

    blocks.append(tmp)

    return blocks


def sumBlocks(block1, block2):
    # SUM TWO BLOCKS
    newElement = 0
    if (len(block1)!=len(block2)):
        print("ERROR: BLOCKS HAVE NOT SAME LENGTH!")
        return 0
    for i in range(0, m):
        newElement = newElement + block1[i] * block2[i]

    return newElement


def multiplyKeyText(key, text):
    # MULTIPLICATION BETWEEN THE KEY AND A TEXT
    result = []
    for i in range(0, len(text)):
        for row in range(0, m):
            result.append(chr(sumBlocks(key[row], text[i]) % 26 + 65))
    return result


def encryption():
    # FUNCTION OF ENCRYPTION
    key = setKey()
    print("STARTING ENCRYPTION...")
    message = readFile("message.txt")
    message = textInBlocks(message)
    cypher = multiplyKeyText(key, message)
    saveText(cypher, "cipher.txt")
    print("ENCRYPTION DONE")
    return cypher



def decryption():
    # FUNCTION OF DECRYPTION
    key = setKey()
    print("STARTING DECRYPTION...")
    cypher = readFile("cipher.txt")
    cypher = textInBlocks(cypher)
    decrypted = multiplyKeyText(inverseMatrix(key), cypher)
    saveText(decrypted, "decryptedMessage.txt")
    print("DECRYPTION DONE")
    return decrypted


def detMatrix(matrix):
    # COMPUTE THE DETERMINANT OF A MATRIX
    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        return diagonalSum(matrix) - antidiagonalSum(matrix)


def diagonalSum(matrix):
    # COMPUTE THE DIAGONAL SUM FOR A MATRIX
    sum = 0
    prod = 1
    for i in range(0, len(matrix)):
        tmp = i
        for j in range(0, len(matrix)):
            prod = prod * matrix[tmp % len(matrix)][j]
            tmp = tmp + 1
        sum = sum + prod
        prod = 1
    return sum


def antidiagonalSum(matrix):
    # COMPUTE THE ANTIDIAGONAL SUM FOR A MATRIX
    sum = 0
    prod = 1
    for i in range(0, len(matrix)):
        tmp = i
        for j in range(len(matrix) - 1, -1, -1):
            prod = prod * matrix[tmp % len(matrix)][j]
            tmp = tmp + 1
        sum = sum + prod
        prod = 1
    return sum


def cofactor(matrix, row, column):
    # COMPUTE THE COFACTOR OF A MATRIX FOR THE POSITION (row, column)
    Cij = []
    tmp = []
    for k in range(0, len(matrix)):
        if k != row:
            for p in range(0, len(matrix[k])):
                if p != column:
                    tmp.append(matrix[k][p])
        if len(tmp) > 0:
            Cij.append(tmp)
            tmp = []

    return pow(-1, row + column) * detMatrix(Cij)


def detModule(det):
    # COMPUTE THE DETERMINANT (MOD 26) FOR THE A^-1 MATRIX
    i = 0
    while True:
        if (det * i) % 26 == 1:
            return i
        else:
            i = i + 1


def inverseMatrix(matrix):
    # COMPUTE THE INVERSE MATRIX
    det = detMatrix(matrix)
    detInv = detModule(det)
    inverse = []
    row = []
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            x = cofactor(matrix, j, i)
            row.append((x * detInv) % 26)
        inverse.append(row)
        row = []
    return inverse


if __name__ == '__main__':

    m = 2
    print(encryption())

    print(decryption())

#  YYPRZWIZJ
