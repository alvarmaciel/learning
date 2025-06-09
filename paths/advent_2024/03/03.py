
def get_input(file_input:str) -> list[list[any]]:
    scaned_lines = []
    with open(file_input, "r") as input:
        scaned_line = [line for line in input]
        scaned_lines.append(scaned_line)
    return scaned_lines


if __name__ == "__main__":
    scaned_memory = get_input("input.txt")
    print(scaned_memory)
