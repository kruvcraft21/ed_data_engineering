# Операция в рамках одной строки: суммирование только абсолютных значений всех чисел, квадрат которых больше 100000.
# Операция для полученного столбца: сортировка столбца по убыванию, вывод топ-10 строк

def write_list(file_name, list):
    with open(file_name, "w", encoding='utf-8') as file:
        for item in list:
            file.write(str(item) + "\n")

with open('second_task.txt', 'r') as file:
    sums = []
    for line in file:
        numbers = map(int, line.split())
        line_sum = sum(abs(num) for num in numbers if abs(num) > 316)
        sums.append(line_sum)

top_sums = sorted(sums, reverse=True)[:10]

write_list('second_task_result.txt', top_sums)