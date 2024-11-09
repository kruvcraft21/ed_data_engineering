import re
from collections import Counter

def write_counter(file_name, list_tuples):
    with open(file_name, 'w') as file:
        for key, value in list_tuples:
            file.write(f"{key}:{value}\n")

def write_list(file_name, list):
    with open(file_name, "w") as file:
        for item in list:
            file.write(str(item) + "\n")


with open('first_task.txt', 'r', encoding='utf-8') as file:
    data = file.read()

words = re.findall(r"\b\w+\b",
                   data.replace("'", "").lower())

words_count = Counter(words).most_common()
print(words_count)
write_counter("first_task_result.txt", words_count)

count_sentences = []
for paragraph in re.split('\n', data):
    if len(paragraph) > 0:
        sentences = re.split(r'[.?!]+', paragraph)
        if len(sentences[-1]) == 0:
            count_sentences.append(len(sentences) - 1)
        else:
            count_sentences.append(len(sentences))

write_list("first_task_var77_result.txt", count_sentences)