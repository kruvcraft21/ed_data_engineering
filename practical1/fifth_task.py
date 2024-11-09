import pandas as pd

table = pd.read_html('fifth_task.html', encoding='utf-8')
table[0].to_csv('fifth_task_result.csv', encoding='utf-8')