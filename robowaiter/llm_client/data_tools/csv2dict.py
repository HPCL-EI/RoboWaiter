import csv
import json

file_name = "test_questions"
# CSV文件的路径
csv_file_path = f'../data_raw/{file_name}.csv'

# Dict输出文件的路径
dict_file_path = f'../data/{file_name}.txt'

output_dict = {}
# 打开CSV文件和JSONL文件
with open(csv_file_path, mode='r', encoding='gbk') as csv_file, \
        open(dict_file_path, mode='w', encoding='utf-8') as jsonl_file:
    # 创建CSV阅读器
    reader = csv.DictReader(csv_file)

    # 遍历CSV文件中的每一行
    for row in reader:
        print(row)
        output_dict[row["Question"]]={"Answer":row["Answer"],"Goal":row["Goal"]}

    # 将每行转换为JSON字符串
    json_str = json.dumps(output_dict, ensure_ascii=False)
    # 将JSON字符串写入JSONL文件，并添加换行符
    jsonl_file.write(json_str + '\n')
