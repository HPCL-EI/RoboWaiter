import json


def print_json(j):
    json_string = json.dumps(j, indent=4)
    print(json_string)






# 假设你有一个名为"data.jsonl"的文件
filename = '../data_raw/train_100_1109.json'
with open(filename, 'r',encoding="utf-8") as file:
    records = eval(file.read())

# 打开一个文件用于写入
with open('../data/train_100_1109.jsonl', 'w', encoding='utf-8') as f:
    for record in records:
        # 将字典转换为JSON字符串，并确保使用UTF-8编码
        json_record = json.dumps(record, ensure_ascii=False)
        # 将JSON字符串写入文件，并添加换行符以分隔记录
        f.write(json_record + '\n')

# record = json.loads(filename)
# print_json(record)

# 打开文件进行读取
# with open(filename, 'r',encoding="gbk") as file:
#     for line in file:
#         # 解析每一行的JSON内容
#         record = json.loads(line)
#         # 现在你可以处理每一个JSON对象（Python字典）
#
#         # 将Python字典转换为格式化的JSON字符串
#         json_string = json.dumps(record, indent=4)
#         print(json_string)