python passage_retrieval2.py \
    --data NQ/test.json   \
    --model_name_or_path ../model/contriever-msmarco \
    --passages psgs_w100.tsv \
    --passages_embeddings "wikipedia_embeddings/*" \
    --output_dir retr_result \
    --n_docs 20

python passage_retrieval2.py --data test_robot.jsonl  --model_name_or_path ../contriever-msmarco --passages train_robot.jsonl --passages_embeddings "robot_embeddings/*" --output_dir retr_result --n_docs 3 --no_fp16