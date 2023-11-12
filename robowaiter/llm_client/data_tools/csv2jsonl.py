import csv
import json

# CSV文件的路径
csv_file_path = 'test_questions.csv'

# JSONL输出文件的路径
jsonl_file_path = '../data/data.jsonl'

# 打开CSV文件和JSONL文件
with open(csv_file_path, mode='r', encoding='gbk') as csv_file, \
        open(jsonl_file_path, mode='w', encoding='utf-8') as jsonl_file:
    # 创建CSV阅读器
    reader = csv.DictReader(csv_file)

    # 遍历CSV文件中的每一行
    for row in reader:
        # 将每行转换为JSON字符串
        json_str = json.dumps(row, ensure_ascii=False)
        # 将JSON字符串写入JSONL文件，并添加换行符
        jsonl_file.write(json_str + '\n')
