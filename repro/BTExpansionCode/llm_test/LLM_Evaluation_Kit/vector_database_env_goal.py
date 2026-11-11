import re
import os
import faiss
import numpy as np
from btpg.utils import ROOT_PATH
from btpg.algos.llm_client.llms.gpt3 import LLMGPT3
from btpg.algos.llm_client.llms.gpt4 import LLMGPT4

# def parse_and_prepare_data(file_path):
#     """从文本文件中解析数据，并生成键值对"""
#     data = {}
#     current_id = None
#
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             line = line.strip()
#             if line.isdigit():
#                 current_id = line
#                 data[current_id] = {"Environment": "", "Goals": "", "Optimal Actions": "", "Vital Action Predicates": "", "Vital Objects": "","Cost":""}
#             else:
#                 match = re.match(r"(\w+(?: \w+)*):\s*(.*)", line)
#                 if match and current_id:
#                     key, value = match.groups()
#                     data[current_id][key.strip()] = value.strip()
#
#     # 将 Environment 和 Goals 组合成键
#     keys = [f"{entry['Environment']}: {entry['Goals']}" for entry in data.values()]
#     return keys, data
def parse_and_prepare_data(file_path):
    """从文本文件中解析数据，并生成键值对"""
    data = {}
    current_id = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.isdigit():
                current_id = line
                data[current_id] = {"Environment": "", "Goals": "", "Optimal Actions": "", "Vital Action Predicates": "", "Vital Objects": "", "Cost": ""}
            else:
                match = re.match(r"(\w+(?: \w+)*):\s*(.*)", line)
                if match and current_id:
                    key, value = match.groups()
                    data[current_id][key.strip()] = value.strip()

    # 去重逻辑：按键值（Environment: Goals）去重
    unique_data = {}
    for key, value in data.items():
        # combined_key = f"{value['Environment']}: {value['Goals']}"
        combined_key = f"{value['Goals']}"
        if combined_key not in unique_data:
            unique_data[combined_key] = value
        else:
            # 如果存在重复项，保留成本较低的项
            if unique_data[combined_key]['Cost'] > value['Cost']:
                unique_data[combined_key] = value

    # 将去重后的数据转换为键值对
    keys = list(unique_data.keys())
    return keys, unique_data


def extract_embedding_vector(response):
    """从 CreateEmbeddingResponse 对象中提取嵌入向量"""
    if response and len(response.data) > 0:
        return response.data[0].embedding
    else:
        raise ValueError("Empty or invalid embedding response.")

# def embed_and_store(llm, keys, data, index_path):
#     """生成嵌入并存储在向量数据库中，同时保存元数据"""
#     embeddings = np.array([extract_embedding_vector(llm.embedding(key)) for key in keys], dtype='float32')
#
#     # 将嵌入和索引保存到 Faiss 索引
#     dim = embeddings.shape[1]
#     index = faiss.IndexFlatL2(dim)
#     index.add(embeddings)
#     faiss.write_index(index, index_path)
#
#     # 保存其他相关数据，包括每个 key 及其对应的 value
#     metadata = [{"key": key, "value": data[key]} for key in data.keys()]
#     np.save(index_path.replace(".index", "_metadata.npy"), metadata)
def embed_and_store(llm, keys, data, index_path):
    """生成嵌入并存储在向量数据库中，同时保存元数据"""
    # 检查现有的索引和元数据文件是否存在
    if os.path.exists(index_path) and os.path.exists(index_path.replace(".index", "_metadata.npy")):
        index = faiss.read_index(index_path)
        metadata = np.load(index_path.replace(".index", "_metadata.npy"), allow_pickle=True).tolist()
    else:
        index = None
        metadata = []

    # 生成新的嵌入向量
    new_embeddings = np.array([extract_embedding_vector(llm.embedding(key)) for key in keys], dtype='float32')

    # 初始化 Faiss 索引
    dim = new_embeddings.shape[1]
    print(dim)
    if index is None:
        index = faiss.IndexFlatL2(dim)

    # 去重逻辑
    for i, key in enumerate(keys):
        duplicate_index = -1
        for j, item in enumerate(metadata):
            if item['key'] == key:
                duplicate_index = j
                break

        new_value = data[key]
        if duplicate_index != -1:
            # 如果存在重复项，比较 cost
            if metadata[duplicate_index]['value']['Cost'] > new_value['Cost']:
                # 更新现有数据
                metadata[duplicate_index]['value'] = new_value
                index.reconstruct(duplicate_index, new_embeddings[i])
        else:
            # 添加新数据
            index.add(new_embeddings[i].reshape(1, -1))
            metadata.append({"key": key, "value": new_value})

    # 保存更新后的索引和元数据
    faiss.write_index(index, index_path)
    np.save(index_path.replace(".index", "_metadata.npy"), metadata)


def search_similar(index_path, llm, environment, goal, top_n=3):
    """搜索与给定环境和目标组合最相似的记录，并输出详细信息"""
    index = faiss.read_index(index_path)
    metadata = np.load(index_path.replace(".index", "_metadata.npy"), allow_pickle=True)

    query = f"{environment}: {goal}"
    query_embedding = np.array([extract_embedding_vector(llm.embedding(query))], dtype='float32')
    distances, indices = index.search(query_embedding, top_n)

    results = [{"id": idx, "distance": dist, "key": metadata[idx]['key'], "value": metadata[idx]['value']}
               for dist, idx in zip(distances[0], indices[0])]
    return results

def check_index_exists(index_path):
    """检查索引文件和元数据文件是否存在"""
    index_file = index_path
    metadata_file = index_path.replace(".index", "_metadata.npy")
    return os.path.exists(index_file) and os.path.exists(metadata_file)

def search_nearest_examples(index_path, llm, goal, top_n=5):
    """检索最接近给定目标的示例"""
    index = faiss.read_index(index_path)
    metadata = np.load(index_path.replace(".index", "_metadata.npy"), allow_pickle=True)

    # env?

    # 获取嵌入向量
    query_embedding = np.array([extract_embedding_vector(llm.embedding(goal))], dtype='float32')
    distances, indices = index.search(query_embedding, top_n)

    # 返回最接近的示例
    nearest_examples = [metadata[idx] for idx in indices[0]]
    return nearest_examples, distances

def add_data_entry(index_path, llm, environment, goal, optimal_actions, vital_action_predicates, vital_objects, cost):
    """添加一条新的数据记录并更新索引，如果有重复项则比较 cost 并选择较小者"""
    # 读取现有数据
    index = faiss.read_index(index_path)
    metadata = np.load(index_path.replace(".index", "_metadata.npy"), allow_pickle=True)

    # 生成新的键和值
    # new_key = f"{environment}: {goal}"
    new_key = f"{goal}"
    new_value = {
        "Environment": environment,
        "Goals": goal,
        "Optimal Actions": optimal_actions,
        "Vital Action Predicates": vital_action_predicates,
        "Vital Objects": vital_objects,
        "Cost": cost
    }

    # 生成新的嵌入向量
    new_embedding = np.array([extract_embedding_vector(llm.embedding(new_key))], dtype='float32')

    # 检查是否存在重复项
    duplicate_index = -1
    for i, item in enumerate(metadata):
        if item['key'] == new_key:
            duplicate_index = i
            break

    if duplicate_index != -1:
        # 如果存在重复项，比较 cost
        if metadata[duplicate_index]['value']['Cost'] > cost:
            # 替换现有数据
            metadata[duplicate_index]['value'] = new_value
            index.reconstruct(duplicate_index, new_embedding[0])
    else:
        # 如果没有重复项，则添加新数据
        index.add(new_embedding)
        metadata = np.append(metadata, [{"key": new_key, "value": new_value}])

    # 保存更新后的索引和元数据
    faiss.write_index(index, index_path)
    np.save(index_path.replace(".index", "_metadata.npy"), metadata)

def write_metadata_to_txt(index_path, output_path):
    """将元数据写入文本文件"""
    metadata = np.load(index_path.replace(".index", "_metadata.npy"), allow_pickle=True)

    with open(output_path, 'w', encoding='utf-8') as file:
        for i, item in enumerate(metadata):
            value = item['value']
            file.write(f"{i + 1}\n")
            file.write(f"Environment:{value['Environment']}\n")
            file.write(f"Instruction:{value.get('Instruction', '')}\n")
            file.write(f"Goals:{value['Goals']}\n")
            file.write(f"Optimal Actions:{value['Optimal Actions']}\n")
            file.write(f"Vital Action Predicates:{value['Vital Action Predicates']}\n")
            file.write(f"Vital Objects:{value['Vital Objects']}\n")
            file.write("\n")

def add_to_database(llm,env, goals, priority_act_ls, key_predicates, key_objects, database_index_path, cost):
    new_environment = "1"
    # new_goal = ' & '.join(goals)
    new_goal=goals
    new_optimal_actions = ', '.join(priority_act_ls)
    new_vital_action_predicates = ', '.join(key_predicates)
    new_vital_objects = ', '.join(key_objects)
    add_data_entry(database_index_path, llm, new_environment, new_goal, new_optimal_actions,
                   new_vital_action_predicates, new_vital_objects, cost)
    print(f"\033[95mAdd the current data to the vector database\033[0m")

def create_empty_index(dimension, index_path):
    index = faiss.IndexFlatL2(dimension)  # 创建一个空的 L2 距离索引
    faiss.write_index(index, index_path)  # 保存空索引到文件
    print(f"Empty index created and saved to {index_path}")

if __name__ == '__main__':
    # 假设 llm 是已经初始化的嵌入模型对象
    llm = LLMGPT3()

    # 示例路径和布尔标志
    # file_path = f"{ROOT_PATH}/../test/dataset/database_cys_5.txt"
    # index_path = f"{ROOT_PATH}/../test/dataset/env_goal_vectors.txt"
    filename = "3"
    # filename = "Group1"
    # filename = "Group01"
    # filename = "DB_rf=3_round9_G0"
    # file_path = f"{ROOT_PATH}/../test/dataset/DATABASE/{filename}.txt"
    # index_path = f"{ROOT_PATH}/../test/dataset/DATABASE/{filename}_env_goal_vectors.index"

    file_path = f"{ROOT_PATH}/../test/VD_3_EXP/DATABASE/{filename}.txt"
    index_path = f"{ROOT_PATH}/../test/VD_3_EXP/DATABASE/{filename}_goal_vectors.index"
    output_path = f"{ROOT_PATH}/../test/VD_3_EXP/DATABASE/DATABASE_{filename}_metadata.txt"

    # filename = "RW_100" #"RHB_100" #"VH_100" #"RHS_100"
    # file_path = f"{ROOT_PATH}/../test/SCENES_EXP/DATABASE/{filename}.txt"
    # index_path = f"{ROOT_PATH}/../test/SCENES_EXP/DATABASE/{filename}_env_goal_vectors.index"
    # output_path = f"{ROOT_PATH}/../test/SCENES_EXP/DATABASE/DATABASE_{filename}_metadata.txt"

    should_rebuild_index = True  # 如果为 True，则重建数据库
    # 检查文件存在或决定是否重建
    if should_rebuild_index or not check_index_exists(index_path):
        # create_empty_index(dimension, index_path)
        keys, data = parse_and_prepare_data(file_path)
        embed_and_store(llm, keys, data, index_path)


    # 将向量数据库里的所有数据写入 txt
    write_metadata_to_txt(index_path, output_path)

    # 输出结果示例
    for key in data:
        print(f"ID: {key}")
        print(f"Environment: {data[key]['Environment']}")
        print(f"Goals: {data[key]['Goals']}")
        print(f"Optimal Actions: {data[key]['Optimal Actions']}")
        print(f"Vital Action Predicates: {data[key]['Vital Action Predicates']}")
        print(f"Vital Objects: {data[key]['Vital Objects']}")
        print(f"Cost: {data[key]['Vital Objects']}")
        print("-----------")

    # 使用特定环境和目标进行查询
    # environment = "IsUnplugged_wallphone, IsUnplugged_coffeemaker, IsUnplugged_lightswitch"
    environment = "1"
    goal = "IsClean_magazine & IsCut_apple & IsPlugged_toaster"
    results = search_similar(index_path, llm, environment, goal)

    # 输出详细检索结果
    for result in results:
        record_id = result['id']
        distance = result['distance']
        key = result['key']
        value = result['value']
        print(f"Record ID: {record_id}, Distance: {distance}")
        print(f"Key: {key}, Value: {value}\n")

    print("=============== 添加新数据后 ================")
    # 测试添加新数据
    # new_environment = "IsUnplugged_tv, IsSwitchedOff_candle, IsClose_window"
    new_environment = "01"
    new_goal = "IsClean_magazine & IsCut_apple & IsPlugged_toaster"
    new_optimal_actions = "Walk_rag, RightGrab_rag, Walk_magazine, Wipe_magazine, Walk_toaster, PlugIn_toaster, RightPutIn_rag_toaster, Walk_kitchenknife, RightGrab_kitchenknife, Walk_apple, LeftGrab_apple, Cut_apple"
    new_vital_action_predicates = "Walk, RightGrab, Wipe, PlugIn, RightPutIn, LeftGrab, Cut"
    new_vital_objects = "rag, magazine, toaster, kitchenknife, apple"

    # add_data_entry(index_path, llm, new_environment, new_goal, new_optimal_actions, new_vital_action_predicates, new_vital_objects)
    #
    # # 再次查询以验证新数据的添加
    # results = search_similar(index_path, llm, new_environment, new_goal)
    # for result in results:
    #     record_id = result['id']
    #     distance = result['distance']
    #     key = result['key']
    #     value = result['value']
    #     print(f"Record ID: {record_id}, Distance: {distance}")
    #     print(f"Key: {key}, Value: {value}\n")
