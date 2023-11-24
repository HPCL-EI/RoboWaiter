#export CUDA_VISIBLE_DEVICES=0
python ../generate_passage_embeddings.py \
        --model_name_or_path ../../model/contriever-msmarco \
        --passages train_robot.jsonl \
        --output_dir robot_embeddings \
        --shard_id 0 \
        --num_shards 1 \
        --per_gpu_batch_size 500


python generate_passage_embeddings.py --model_name_or_path ../contriever-msmarco --passages train_robot.jsonl --output_dir robot_embeddings --shard_id 0 --num_shards 1 --per_gpu_batch_size 500 --no_fp16