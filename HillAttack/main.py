import math as mt

m = 0

def attack():
    print("STARTING ATTACK...")
    message, i = obtainMatrix("message.txt")
    cipher = obtainMatrix("cipher.txt", i)
    if message == 0:
        print("UNUSABLE MESSAGE FOR ATTACK")
        return 0
    if cipher == 0:
        print("UNUSABLE CYPHER FOR ATTACK")
        return 0
    matrixKey = matrixProduct(cipher, inverseMatrix(message))   # K = C P^-1
    print("ATTACK DONE")

    return (blocksToString(matrixKey), matrixKey)


def readFile(fileName):
    # READ THE CONTENT OF A FILE AND PUT INTO AN ARRAY
    file = open(fileName, "r")
    words = file.read().splitlines()
    file.close()
    return list(words[0])


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


def blocksToString(blocks):
    # TRANSFORM A LIST OF BLOCK TO STRING
    result = []
    for i in range(0, m):
        for j in range(0, m):
            result.append(chr(blocks[i][j] % 26 + 65))
    return "".join(result)


def obtainMatrix(fileName, cipher=-1):
    # READ TEXT FROM FILE AND CONSTRUCT AN USABLE MATRIX FOR ATTACK
    text = readFile(fileName)
    text = textInBlocks(text)
    if cipher != -1:
        return constructMatrix(text, cipher)
    matrixText = getInvertibleMatrix(text)
    return matrixText


def getInvertibleMatrix(text):
    # SEARCH AMONG THE BLOCKS THOSE THAT ARE USEFUL TO BUILD THE MATRIX THE ATTACK
    matrix = constructMatrix(text, 0)
    i = 1
    while matrix != 0 and hasInverse(matrix) == 0:    # VERIFY IF THE MATRIX IS INVERTIBLE
        matrix = constructMatrix(text, i)
        i = i + 1
    return (matrix, i - 1)


def hasInverse(matrix):
    # VERIFY IF A MATRIX HAS AN INVERSE
    det = detMatrix(matrix) % 26
    if det == 0 or mt.gcd(det, 26) != 1:
        return 0
    else:
        return 1

def constructMatrix(message, k):
    # FROM A LIST OF BLOCKS CONSTRUCT AN mxm MATRIX
    matrix = []
    tmp = []
    if len(message) < m + k:
        return 0
    for j in range(0, m):
        for i in range(k, m + k):
            tmp.append(message[i][j])
        matrix.append(tmp)
        tmp = []
    return matrix

def matrixProduct(matrix1, matrix2):
    # COMPUTE THE PRODUCT BETWEEN TWO MATRICES
    newMatrix = []
    tmp = []
    for r in range(0, m):
        for c in range(0, m):
            sum = 0
            for k in range(0, m):
                sum = sum + matrix1[r][k] * matrix2[k][c]
            tmp.append(sum % 26)
        newMatrix.append(tmp)
        tmp = []

    return newMatrix


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

    key = attack()
    if (key != 0):
        print(f"KEY IN MATRICAL FORM IS --> {key[1]}")
        print(f"THE KEY IS--> {key[0]}")
