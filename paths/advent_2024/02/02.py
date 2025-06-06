
def get_reports_lines(file_input:str) -> list[list[int]]:
    reports_list = []

    with open(file_input, "r") as input:
        for line in input:
            report_line = [int(number) for number in line.split()]
            reports_list.append(report_line)
    return reports_list


def get_amount_of_safe_reports(report_list: list[list[int]]) -> int:
    safe_collector = 0
    for report_line in reports_list:
        safety_report = create_safety_report(report_line)
        if all(safety_report):
            safe_collector += 1
            continue
        # else:
        #     # remuevo cada nro y probamos
        #     # Pruebo
        #     new_report = report_line.copy()
        #     for i in range(len(new_report)):
        #         dumped_report = create_safety_report(new_report[0:i]+new_report[i+1:])
        #         if all(dumped_report):
        #             safe_collector += 1
        #             break

    return safe_collector


def create_safety_report(report_line:list[int]) -> list[bool]:

    safety_levels = []

    for i, number in enumerate(report_line):

        # check sort and order
        crescient = all(report_line[a] <= report_line[a+1] for a in range(len(report_line)-1))
        # repeated or unordered item on list

        if i != len(report_line)-1:
            if crescient and number >= report_line[i+1]:
                safety_levels.append(False)
                continue
            if not crescient and number <= report_line[i+1]:
                safety_levels.append(False)
                continue

            difference = abs(number - report_line[i+1])
        else:
            difference = abs(number - report_line[i-1])

        if difference <= 3:
            safety_levels.append(True)
            continue
        else:
            safety_levels.append(False)
            continue

    return safety_levels


if __name__ == "__main__":
    reports_list = get_reports_lines("test.txt")
    amount_of_safe_reports = get_amount_of_safe_reports(reports_list)
    print(amount_of_safe_reports)
