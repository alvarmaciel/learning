from pathlib import Path

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

def count_xmas(matrix):
    n = len(matrix)
    m = len(matrix[0]) if n > 0 else 0
    count = 0
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if matrix[i][j] != 'A':
                continue
            # ↖ (i-1,j-1), ↘ (i+1,j+1)
            d1 = matrix[i - 1][j - 1] + 'A' + matrix[i + 1][j + 1]
            # ↗ (i-1,j+1), ↙ (i+1,j-1)
            d2 = matrix[i - 1][j + 1] + 'A' + matrix[i + 1][j - 1]
            if (d1 == 'MAS' or d1 == 'SAM') and (d2 == 'MAS' or d2 == 'SAM'):
                count += 1
    return count

if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"
    matrix = get_soup(str(input_path))
    xmas_count = count_xmas(matrix)
    print(xmas_count)
