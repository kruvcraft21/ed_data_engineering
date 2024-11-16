# Подсчитайте сумму всех элементов и их среднее арифметическое, подсчитайте сумму и
# среднее арифметическое главной и побочной диагоналей матрицы.
# Найдите максимальное и минимальное значение.

import numpy as np
import json

data : np.ndarray = np.load("first_task.npy")
result = {
    "sum": 0,
    "avr": 0,
    "sumMD": 0,
    "avrMD": 0,
    "sumSD": 0,
    "avrSD": 0,
    "max": 0,
    "min": 0
}

rows, cols = data.shape

for i in range(rows):
    for j in range(cols):
        value = int(data[i, j])
        result['sum'] += value
        if i == j:
            result["sumMD"] += value
        if i + j == cols - 1:
            result["sumSD"] += value


result["avr"] = result["sum"] / data.size
result["avrMD"] = result["sumMD"] / min(rows, cols)
result["avrSD"] = result['sumSD'] / min(rows, cols)
result["min"] = float(data.min())
result["max"] = float(data.max())

with open("first_task_result.json", "w") as file:
    json.dump(result, file, indent=4)

# Исходную матрицу необходимо нормализовать и сохранить в формате npy. 

normalize_data = data / result["sum"]
np.save("first_task_normalized.npy", normalize_data)