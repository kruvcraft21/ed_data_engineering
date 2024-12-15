import pandas as pd
import os, json
import matplotlib.pyplot as plt

# Источник данных https://www.kaggle.com/datasets/aleespinosa/soccer-match-event-dataset?select=actions.csv
# Загружен был только actions.csv

def get_size_from_disk(file_name: str) -> int:
    return os.path.getsize(file_name)

def bytes2mb(bytes:int) -> int:
    return bytes//(1024*1024)

def analyze_data(data_frame: pd.DataFrame):
    memory_usage = data_frame.memory_usage(deep=True)
    total_memory = memory_usage.sum()
    column_stats = []

    for column in data_frame.columns:
        col_mem = memory_usage[column]
        col_type = data_frame[column].dtype
        column_stats.append({
            "column": column,
            "memory": int(col_mem),
            "memory_fraction": float(col_mem / total_memory),
            "dtype": str(col_type)
        })

    column_stats = sorted(column_stats, key=lambda x: x['memory'], reverse=True)
    return total_memory, column_stats

def list_to_json(list_of_dict, file_name):
    with open(file_name, "w") as f:
        json.dump(list_of_dict, f, ensure_ascii=False, indent=4)

def optimize_object_columns(data_frame: pd.DataFrame):
    for column in data_frame.select_dtypes(include=['object']).columns:
        if data_frame[column].nunique() / len(data_frame[column]) < 0.5:
            data_frame[column] = data_frame[column].astype('category')

def optimize_numeric_columns(data_frame: pd.DataFrame):
    for column in data_frame.select_dtypes(include=['int']).columns:
        data_frame[column] = pd.to_numeric(data_frame[column], downcast='integer')

    for column in data_frame.select_dtypes(include=['float']).columns:
        data_frame[column] = pd.to_numeric(data_frame[column], downcast='float')


def chunked_load(file_path, columns, chunk_size, output_file, dtypes):
    selected_chunks = []
    for chunk in pd.read_csv(file_path, usecols=columns, chunksize=chunk_size, dtype=dtypes):
        selected_chunks.append(chunk)

    result_df = pd.concat(selected_chunks, ignore_index=True)
    result_df.to_csv(output_file, index=False)
    return result_df

def plot_graphs(data_frame: pd.DataFrame):
    # Линейный график
    plt.figure(figsize=(10, 5))
    data_frame["start_x"].head(100).plot(kind='line')
    plt.show()

    # Столбчатая диаграмма
    plt.figure(figsize=(10, 5))
    data_frame["type_name"].value_counts().plot(kind='bar', title="Распределение категорий")
    plt.xlabel("Категория")
    plt.ylabel("Количество")
    plt.show()

    # Круговая диаграмма
    plt.figure(figsize=(8, 8))
    data_frame["result_name"].value_counts().plot(kind='pie')
    plt.show()

    # Корреляционная матрица
    plt.figure(figsize=(10, 8))
    numeric_df = data_frame.select_dtypes(include=['number'])  # Только числовые колонки
    corr_matrix = numeric_df.corr()
    plt.matshow(corr_matrix, fignum=1)
    plt.colorbar()
    plt.show()

    # Распределение переменной
    plt.figure(figsize=(10, 5))
    data_frame["time_seconds"].plot(kind='hist')
    plt.xlabel("Время")
    plt.ylabel("Частота")
    plt.show()

dataset = 'actions.csv'
data = pd.read_csv(dataset, index_col=0)

print(f"2.a Объем памяти, который занимает файл на диске: {bytes2mb(get_size_from_disk(dataset))} MB")
total_memory, column_stats = analyze_data(data)
print(f"2.b Объем памяти, который занимает набор данных при загрузке в память: {bytes2mb(total_memory)} MB")
print("2.c Объем памяти, доля от общего объема, тип данных")
print(column_stats)
print("3. Вывод статистики в json: original_stat.json")
list_to_json(column_stats, "original_stat.json")
print("4. Преобразование всех колонок с типом данных «object» в категориальные, если количество уникальных значений колонки составляет менее 50%")
optimize_object_columns(data)
print("5. Понижающее преобразование типов «int» колонок")
print("6. Понижающее преобразование типов «float» колонок")
optimize_numeric_columns(data)
print("7. Повторный анализ данных как в п.2")
total_memory_modify, column_stats_modify = analyze_data(data)
print(f"Размер измененного датасета {bytes2mb(total_memory_modify)} MB")
print(f"Разница с оригинальным датасетом {bytes2mb(total_memory - total_memory_modify)} MB")
print(column_stats_modify)
list_to_json(column_stats_modify, "column_stats_modify.json")
print("8. Чанковая загрузка 10 колонок")
selected_columns = ["game_id", "time_seconds", "team_id", "player_id", "start_x", "start_y", "end_x", "end_y", "type_name", "result_name"]
subset_data = chunked_load(dataset, selected_columns, chunk_size=1000, output_file="subset_data.csv", dtypes=data[selected_columns].dtypes.to_dict())
print("9. Построение графиков")
plot_graphs(subset_data)