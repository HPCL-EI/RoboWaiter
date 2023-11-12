import csv

# CSV文件的路径
csv_file_path = 'test_questions.csv'

# 要写入CSV文件的数据，每个元素是一行
rows = [
    ["Question", "Answer", "Goal"],  # 表头
    ["Alice", "24", "New York"],
    ["Bob", "30", "San Francisco"],
    ["Charlie", "18", "Los Angeles"]
]

# 打开（或创建）文件进行写入
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    # 创建一个CSV写入器
    writer = csv.writer(file)

    # 写入数据
    for row in rows:
        writer.writerow(row)

print(f"CSV file '{csv_file_path}' created successfully.")
