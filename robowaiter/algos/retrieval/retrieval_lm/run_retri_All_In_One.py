import os
from robowaiter.algos.retrieval.retrieval_lm.question2jsonl import question2jsonl,question2jsonl_test

file_path = "fix_questions.txt"
output_path = "fix_questions.jsonl"
output_test_path = "fix_questions_test.jsonl"

question2jsonl(file_path,output_path)
question2jsonl_test(file_path,output_test_path)

# path_goal_states_with_description = os.path.join('../../../behavior_tree/dataset/goal_states_with_description.jsonl')
#
# cmd_goal_states_with_descrip_to_train = f' .\process_json.py --passages {path_goal_states_with_description} --mode train'


# cmd_goal_states_with_descrip_to_test = f" .\process_json.py --passages .\\train_robot.jsonl --mode test"
cmd_get_embedding = f" generate_passage_embeddings.py --model_name_or_path ../contriever-msmarco --passages {output_path} --output_dir robot_embeddings --shard_id 0 --num_shards 1 --per_gpu_batch_size 500 --no_fp16"
cmd_test_retri = f" passage_retrieval2.py --data {output_test_path}  --model_name_or_path ../contriever-msmarco --passages {output_path} --passages_embeddings \"robot_embeddings/*\" --output_dir retr_result --n_docs 3 --no_fp16"

# conda_path = os.path.join("C:/Users/Estrella/.conda/envs/py310/python.exe")
# os.system(conda_path + cmd_goal_states_with_descrip_to_train)
# os.system(conda_path + cmd_goal_states_with_descrip_to_test)
os.system("python " + cmd_get_embedding)
os.system("python " + cmd_test_retri)
