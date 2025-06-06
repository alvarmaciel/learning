# Parse file and create two list
file_input = "01input.txt"
list_1 = []
list_2 = []
with open(file_input, "r") as input:
    for line in input:
        id_line = line.split(" ")
        list_1.append(int(id_line[0]))
        list_2.append(int(id_line[-1]))
# Sort each list
list_1.sort()
list_2.sort()
# Compara one to one calculate absolute diference and save it una collector
result = 0
for i in range(len(list_1)):
    difference = list_1[i] - list_2[i]
    result = result + abs(difference)
print(result)
similiraty = 0
similiraty_score = 0
for number in list_1:
    score = list_2.count(number)
    similiraty = number * score
    similiraty_score = similiraty_score + similiraty
print(similiraty_score)
