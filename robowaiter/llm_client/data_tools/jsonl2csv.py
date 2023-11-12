import json
import csv

data_name = "train_100_1109"
jsonl_data = f"../data_raw/{data_name}.csv"
csv_file_path = f"../data/{data_name}.csv"

# 转换函数
def convert_json_to_csv(json_data, csv_file_path):
    # CSV文件的路径
    # 打开（或创建）文件进行写入
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        # 创建一个CSV写入器
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(["Question", "Answer", "Goal"])

        # 提取Question, Answer, Goal 并写入CSV
        for round in json_data["chat_rounds"]:
            if round["role"] == "human":
                # 提取Question
                question = round["content"].split('\nchat_list: ')[0].replace('State: ', '').strip()
            elif round["role"] == "bot":
                # 提取Answer和Goal
                answer = round["content"].split('\nGoals: ')[0].replace('Response: ', '').strip()
                goal = round["content"].split('\nGoals: ')[1].strip()
                # 写入到CSV文件
                writer.writerow([question, answer, goal])
