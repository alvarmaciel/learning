def get_soup(file_input:str) -> str:
    matrix = []

    with open(file_input, "r") as input:
        for line in input:
            row=[]
            for charac in line:
                if charac != '\n':
                    row.append(charac)
            matrix.append(row)

    return matrix

def count_words(matrix: [[str]]) -> int:
    rows = len(matrix)
    col = len(matrix[0]) if rows > 0 else 0
    word = 'XMAS'
    reverse_word = 'SAMX'
    count = 0
    directions = [
        (0, 1), # Derecha
        (0, -1), # izquierda
        (1, 0), # abajo
        (-1, 0), # arriba
        (1,1), # diagonal inferior derecha
        (-1,-1), # diagonal superior izquierda
        (1,-1), # Diagonal inferior izquierda
        (-1,1) # diagonal superior derecha
    ]

    for i in range(rows):
        for j in range(col):
            for di, dj in directions:
                matched = True
                for k in range(4):
                    ni, nj = i + di * k, j + dj * k
                    if 0 <= ni < rows and 0 <= nj < col:
                        if matrix[ni][nj] != word[k]:
                            matched = False
                            break
                    else:
                        matched = False
                        break
                if matched:
                    count +=1

                # verificar invertida
                # matched = True
                # for k in range(4):
                #     ni, nj = i + di * k, j + dj * k
                #     if 0 <= ni < rows and 0 <= nj < col:
                #         if matrix[ni][nj] != reverse_word[k]:
                #             matched = False
                #             break
                #     else:
                #         matched = False
                #         break
                # if matched:
                #     count +=1
    return count

if __name__ == "__main__":
    matrix = get_soup("input.txt")
    xmas_count = count_words(matrix)
    print(xmas_count)
