import copy
import re
import spacy
nlp_en = spacy.load('en_core_web_lg')

reply = "at(coffee,Table)"
# 正则表达式
replay_words = re.sub(r'[^A-Za-z0-9]', ' ', reply)
replay_words = replay_words.split() #['at','coffee','Table']

noun_words_ls = [['At','On','Is'],[]]# 完整文档n*2(动作，单词)
together_words_ls = []
# 示例代码：如何使用Python逐行读取txt文件
# 打开一个示例的txt文件（这里假设文件名为example.txt）
file_path = './goal_states_unique.txt'
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        # 逐行读取文件
        for line in file:
            cleaned_line = re.sub(r'[^A-Za-z0-9]', ' ', line)
            words = cleaned_line.split()
            # print(words)
            noun_words_ls[-1].extend(words)
            # print(line.strip())  # 打印每一行内容，去除行尾的换行符

            cleaned_line = line.replace("{", "").replace("}", "").replace("\n", "")
            together_words_ls.append(cleaned_line)

except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")


# 建立语料库

file_path = './goal_states_unique.txt'
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        # 逐行读取文件
        for line in file:
            cleaned_line = re.sub(r'[^A-Za-z0-9]', ' ', line)
            words = cleaned_line.split()
            # print(words)
            noun_words_ls[-1].extend(words)
            # print(line.strip())  # 打印每一行内容，去除行尾的换行符

            cleaned_line = line.replace("{", "").replace("}", "").replace("\n", "")
            together_words_ls.append(cleaned_line)

except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")



# import datetime
# from gensim.models import word2vec
# import numpy as np
# from scipy import spatial
# pre_time=datetime.datetime.now()
# model = word2vec.Word2Vec(together_words_ls,
#         vector_size=10,#特征向量的维度
#         alpha=0.04,#学习率
#         window=5,#一个句子内，当前词和预测词之间的最大距离 文本（window）大小：skip-gram通常在10附近，CBOW通常在5附近
#         min_count=0,#最低词频  没有大的变化
#         max_vocab_size=None,
#         sample=0.0001, #随机下采样的阈值
#         seed=1,#随机数种子
#         workers=10,#进程数
#         min_alpha=0.00001,#学习率下降的最小值
#         sg=1, #训练算法的选择，sg=1，采用skip-gram，sg=0，采用CBOW---skip-gram（慢、对罕见字有利）vs CBOW（快）
#         hs=1,# hs=1,采用hierarchica·softmax，hs=0,采用negative sampling
#             #分层softmax（对罕见字有利）vs 负采样（对常见词和低纬向量有利）
#         negative=0,#这个值大于0，使用negative sampling去掉'noise words'的个数（通常设置5-20）；为0，不使用negative sampling
#         #cbow_mean=1,#为0，使用词向量的和，为1，使用均值；只适用于cbow的情况
#         null_word = 0,
#         trim_rule = None, #裁剪词汇规则，使用None（会使用最小min_count）
#         sorted_vocab =1,#对词汇降序排序
#         batch_words = 8192,#训练时，每一批次的单词数量
#         compute_loss = False,
#         callbacks = ())
# model.train(together_words_ls, total_examples=len(together_words_ls), epochs=10)
# model.save("./W2V_CI.model")  # 保存模型
# post_time=datetime.datetime.now()
# print("word2vec模型训练保存结束，时间为: ",(post_time-pre_time).seconds*1.0)#1106.0s
#
# w2v_model = word2vec.Word2Vec.load("./W2V_CI.model")
# # w2v_model[word]
#
# def replay_together_w2v(reply):
#     return model.wv.most_similar(reply)
#     # max_similarity = -1
#     # similar_word = None
#     # query_token = w2v_model[reply]
#     # for state in together_words_ls:
#     #     word_token = w2v_model[state]
#     #     # 计算余弦相似度. spatial.distance.cosine 函数计算的是余弦距离
#     #     # 余弦相似度（Cosine similarity），如在 Word2Vec 模型中用来比较两个向量的相似性，其值的范围是 -1 到 1。
#     #     similarity = 1 - spatial.distance.cosine(query_token, word_token)
#     #     # print("similarity:",similarity,real_obj_name)
#     #     if similarity > max_similarity:
#     #         max_similarity = similarity
#     #         similar_word = state
#     # if similar_word==None:
#     #     print("Error: Not Match!")
#     # else:
#     #     return similar_word



def replay_one_by_one(replay_words):
    replace_ind = []
    replace_word = []
    for i,word in enumerate(replay_words):
        query_token = nlp_en(word)
        k=1
        if i==0: k=0
        if not word in noun_words_ls[k]:
            max_similarity = 0
            similar_word = None
            for act in noun_words_ls[k]:
                word_token = nlp_en(act)
                # print(act)
                # print(word_token)
                similarity = query_token.similarity(word_token)
                # print("similarity:",similarity,real_obj_name)
                if similarity > max_similarity:
                    max_similarity = similarity
                    similar_word = act
            if similar_word==None:
                print("Error: Not Match!")
            else:
                replay_words[i]=similar_word
                # replace_word.append(similar_word)
                # replace_ind.append(i)
    new_replay = f'{replay_words[0]}({replay_words[1]},{replay_words[2]})'
    return new_replay

    # print(replace_word)
    # print(replace_ind)
    # replace_word = ['on','Table1']
    # replace_ind = [0,2]
    # 替换reply中单词
    # for new_word,ind in zip(replace_word,replace_ind):
        # 把第 ind 个单词替换成 new_word

def replay_together(reply):
    max_similarity = 0
    similar_word = None
    query_token = nlp_en(reply)
    for state in together_words_ls:
        word_token = nlp_en(state)
        similarity = query_token.similarity(word_token)
        # print("similarity:",similarity,real_obj_name)
        if similarity > max_similarity:
            max_similarity = similarity
            similar_word = state
    if similar_word==None:
        print("Error: Not Match!")
    else:
        return similar_word

print("原来的：",reply)
new_replay = replay_one_by_one(copy.deepcopy(replay_words))
print("逐个比较后的现在的：",new_replay)
new_replay2 = replay_together(copy.deepcopy(reply))
print("集体比较后的现在的：",new_replay2)
# new_replay3 = replay_together_w2v(copy.deepcopy(reply))
# print("W2V比较后的现在的：",new_replay3)

