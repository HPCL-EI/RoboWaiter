python passage_retrieval3.py \
    --model_name_or_path ../model/contriever-msmarco \
    --passages train_robot.jsonl \
    --passages_embeddings "robot_embeddings/*" \
    --data test_robot.jsonl \
    --output_dir robot_result \
    --n_docs 2


#python passage_retrieval3.py --model_name_or_path contriever-msmarco --passages train_robot.jsonl --passages_embeddings "robot_embeddings/*"  --data test_robot.jsonl  --output_dir robot_result --n_docs 2