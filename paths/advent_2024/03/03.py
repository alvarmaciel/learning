import re

def get_input(file_input:str) -> str:

    with open(file_input, "r") as input:
        scaned_file = input.read()
    return scaned_file


def get_mul_fragment(scaned_memory:str) -> list[(int, int)]:

    pattern = r'\bmul\((\d{1,3}),(\d{1,3})\)'
    findings = re.findall(pattern, scaned_memory)

    findings_as_int = [(int(a), int(b)) for a, b in findings]

    return findings_as_int


def get_sum_of_mul(mul_fragment: str) -> int:
    list_of_mul = [a*b for a,b in mul_fragment]
    return sum(list_of_mul)


if __name__ == "__main__":
    scaned_memory = get_input("input.txt")
    mul_fragment = get_mul_fragment(scaned_memory)
    sum_of_the_mul = get_sum_of_mul(mul_fragment)
    print(sum_of_the_mul)
