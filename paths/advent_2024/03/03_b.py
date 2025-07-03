import re

def get_input(file_input:str) -> str:

    with open(file_input, "r") as input:
        scaned_file = input.read()
    return scaned_file


def scan_memory(scaned_memory:str) -> list[(int, int)]:
    pattern = r"(do\(\))|(don't\(\))|mul\((\d{1,3}),(\d{1,3})\)"
    enabled = True
    results = []
    for match in re.finditer(pattern, scaned_memory):
        if match.group(1): # do()
            enabled = True
        elif match.group(2): # don´t()
            enabled = False
        elif match.group(3): # mul()
            if enabled:
                results.append((int(match.group(3)), int(match.group(4))))
    return results




def get_sum_of_mul(mul_fragment) -> int:

    list_of_mul = [a*b for a,b in mul_fragment]
    return sum(list_of_mul)


if __name__ == "__main__":
    scaned_memory = get_input("input.txt")
    fragments = scan_memory(scaned_memory=scaned_memory)
    sum_of_the_mul = get_sum_of_mul(fragments)
    print(sum_of_the_mul)
