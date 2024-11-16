# Найти публичный API, который возвращает JSON с некоторыми данными. 
# Необходимо получить данные в формате JSON, преобразовать в html представление в зависимости от содержания.

import requests

# Получаем JSON-данные от API
response = requests.get("https://official-joke-api.appspot.com/random_ten")
data = response.json()

# Создаем HTML-контент с карточками
html_content = """
<html>
<head>
    <title>Jokes</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; flex-wrap: wrap; justify-content: center; background-color: #f4f4f9; }
        .card {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            width: 300px;
            margin: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .card h3 { font-size: 1.2em; color: #333; }
        .card p { color: #555; }
        .card .punchline { font-weight: bold; color: #333; margin-top: 10px; }
    </style>
</head>
<body>
    <h1 style="width: 100%; text-align: center;">Jokes</h1>
"""

# Заполняем карточки шутками
for joke in data:
    html_content += f"""
    <div class="card">
        <h3>Type: {joke['type'].capitalize()}</h3>
        <p><strong>Q:</strong> {joke['setup']}</p>
        <p class="punchline"><strong>A:</strong> {joke['punchline']}</p>
    </div>
    """

# Завершаем HTML-документ
html_content += """
</body>
</html>
"""

# Записываем HTML в файл
with open("sixth_task_result.html", "w", encoding="utf-8") as file:
    file.write(html_content)