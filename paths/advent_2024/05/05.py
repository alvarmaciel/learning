# create a list of tuples with first part
# create a list of posibles results
# compare by 2 each result with the list of tuples and define if is true
# find middle y sum
from  pathlib import Path

def get_processed_file(file_path:str) ->([(int,int)],[[int]]):
    rules = []
    pages_to_print = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if "|" in line:
                rules.append((int(line.split("|")[0]),int(line.split("|")[1])))
            else:
                number_list = [int(num) for num in line.split(",") if num]
                pages_to_print.append(number_list)

    return rules, pages_to_print

def get_middles_pages_if_valid(rules:[(int,int)], pages_to_print[[int]]) -> [[int]]:
    # get valid list of pages
    valid_list_of_pages = get_valid_list_of_pages(rules, pages_to_print)


def get_valid_list_of_pages(rules, pages_to_print):
    # para cada lista de pagina
    # comparar cada tupla de rules con las 2 valores
if __name__ == "__main__":
    input_path = Path(__file__).parent / "test.txt"
    rules, pages_to_print = get_processed_file(str(input_path))
    middles_pages = get_middles_pages_if_valid(rules, pages_to_print)
