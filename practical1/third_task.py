# Считайте файл согласно вашему варианту. 
# В строках имеются пропуски, обозначенные «N/A» – замените их, рассчитав среднее значение соседних чисел.
# Оставляем положительные значения, квадрат которых не превышает 2500
# Среднее по каждой строке

def fill_na_avenger(numbers):
    for i in range(len(numbers)):
        if numbers[i] == "N/A":
            is_left = 1 if i > 0 else 0
            is_right = 1 if i < len(numbers) - 1 else 0
            new_number = 0.0
            if is_left != 0:
                new_number += int(numbers[i - 1])
            if is_right != 0:
                new_number += int(numbers[i + 1])
            new_number /= (is_left + is_right)
            numbers[i] = new_number
        else:
            numbers[i] = int(numbers[i])
    return numbers

def filter_number_77(numbers):
    return [num for num in numbers if num > 0 and num**2 <= 2500]

def applay_operation_77(numbers):
    count_nums = len(numbers)
    sum_nums = sum(numbers)
    return 0 if count_nums == 0 else sum_nums / count_nums

def write_list(file_name, list):
    with open(file_name, "w", encoding='utf-8') as file:
        for item in list:
            file.write(str(item) + "\n")

with open("third_task.txt", 'r', encoding='utf-8') as file:
    table = []
    for line in file:
        cleared_line = fill_na_avenger(line.split())
        filtered_line = filter_number_77(cleared_line)
        table.append(filtered_line)

table = [applay_operation_77(numbers) for numbers in table]

write_list("third_task_result.txt", table)