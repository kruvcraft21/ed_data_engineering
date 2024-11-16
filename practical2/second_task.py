# Отберите из матрицы значения, которые превышают следующее значение: 577,
# следующим образом: индексы элемента разнесите по массивам x, y, а само значение в массив z.

import numpy as np
import os

data : np.ndarray = np.load('second_task.npy')

x = []
y = []
z = []

rows, cols = data.shape

FILTER_VALUE = 577

for i in range(rows):
    for j in range(cols):
        if data[i, j] > FILTER_VALUE:
            x.append(i)
            y.append(j)
            z.append(data[i, j])

# Сохраните полученные массив в файла формата npz. Воспользуйтесь методами np.savez() и np.savez_compressed().
# Сравните размеры полученных файлов

np.savez('second_task.npz', x=x, y=y, z=z)
np.savez_compressed('second_task_compressed.npz', x=x, y=y, z=z)

npz_size = os.path.getsize('second_task.npz')
npz_comp_size = os.path.getsize('second_task_compressed.npz')
print(f"Разница в размерах {npz_size / npz_comp_size}")
# Разница в размерах 3.384126984126984