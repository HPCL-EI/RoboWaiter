# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import argparse
import csv
import json
import logging
import pickle
import time
import glob
from pathlib import Path

import numpy as np
import torch
import transformers

import robowaiter.algos.retrieval.retrieval_lm.src.index
import robowaiter.algos.retrieval.retrieval_lm.src.contriever
import robowaiter.algos.retrieval.retrieval_lm.src.utils
import robowaiter.algos.retrieval.retrieval_lm.src.slurm
import robowaiter.algos.retrieval.retrieval_lm.src.data
from robowaiter.algos.retrieval.retrieval_lm.src.evaluation import calculate_matches
import robowaiter.algos.retrieval.retrieval_lm.src.normalize_text
from robowaiter.algos.retrieval.retrieval_lm import src


os.environ["TOKENIZERS_PARALLELISM"] = "true"


def embed_queries(args, queries, model, tokenizer):
    model.eval()
    embeddings, batch_question = [], []
    with torch.no_grad():

        for k, q in enumerate(queries):
            if args.lowercase:
                q = q.lower()
            if args.normalize_text:
                q = src.normalize_text.normalize(q)
            batch_question.append(q)

            if len(batch_question) == args.per_gpu_batch_size or k == len(queries) - 1:

                encoded_batch = tokenizer.batch_encode_plus(
                    batch_question,
                    return_tensors="pt",
                    max_length=args.question_maxlength,
                    padding=True,
                    truncation=True,
                )
                encoded_batch = {k: v for k, v in encoded_batch.items()}
                output = model(**encoded_batch)
                embeddings.append(output.cpu())

                batch_question = []

    embeddings = torch.cat(embeddings, dim=0)
    print(f"Questions embeddings shape: {embeddings.size()}")

    return embeddings.numpy()


def index_encoded_data(index, embedding_files, indexing_batch_size):
    allids = []
    allembeddings = np.array([])
    for i, file_path in enumerate(embedding_files):
        print(f"Loading file {file_path}")
        with open(file_path, "rb") as fin:
            ids, embeddings = pickle.load(fin)

        allembeddings = np.vstack((allembeddings, embeddings)) if allembeddings.size else embeddings
        allids.extend(ids)
        while allembeddings.shape[0] > indexing_batch_size:
            allembeddings, allids = add_embeddings(index, allembeddings, allids, indexing_batch_size)

    while allembeddings.shape[0] > 0:
        allembeddings, allids = add_embeddings(index, allembeddings, allids, indexing_batch_size)

    print("Data indexing completed.")


def add_embeddings(index, embeddings, ids, indexing_batch_size):
    end_idx = min(indexing_batch_size, embeddings.shape[0])
    ids_toadd = ids[:end_idx]
    embeddings_toadd = embeddings[:end_idx]
    ids = ids[end_idx:]
    embeddings = embeddings[end_idx:]
    index.index_data(ids_toadd, embeddings_toadd)
    return embeddings, ids


def validate(data, workers_num):
    match_stats = calculate_matches(data, workers_num)
    top_k_hits = match_stats.top_k_hits

    print("Validation results: top k documents hits %s", top_k_hits)
    top_k_hits = [v / len(data) for v in top_k_hits]
    message = ""
    for k in [5, 10, 20, 100]:
        if k <= len(top_k_hits):
            message += f"R@{k}: {top_k_hits[k-1]} "
    print(message)
    return match_stats.questions_doc_hits


def add_passages(data, passages, top_passages_and_scores):
    # add passages to original data
    merged_data = []
    assert len(data) == len(top_passages_and_scores)
    for i, d in enumerate(data):
        results_and_scores = top_passages_and_scores[i]
        docs = [passages[int(doc_id)] for doc_id in results_and_scores[0]]
        scores = [str(score) for score in results_and_scores[1]]
        ctxs_num = len(docs)
        d["ctxs"] = [
            {
                "id": results_and_scores[0][c],
                "title": docs[c]["title"],
                "text": docs[c]["text"],
                "score": scores[c],
            }
            for c in range(ctxs_num)
        ]


def add_hasanswer(data, hasanswer):
    # add hasanswer to data
    for i, ex in enumerate(data):
        for k, d in enumerate(ex["ctxs"]):
            d["hasanswer"] = hasanswer[i][k]


def load_data(data_path):
    if data_path.endswith(".json"):
        with open(data_path, "r") as fin:
            data = json.load(fin)
    elif data_path.endswith(".jsonl"):
        data = []
        with open(data_path, "r",encoding='utf-8') as fin:
            for k, example in enumerate(fin):
                example = json.loads(example)
                data.append(example)
    return data

parser = argparse.ArgumentParser()

parser.add_argument(
    "--data",
    type=str,
    default=None,
    help=".json file containing question and answers, similar format to reader data",
)
parser.add_argument("--passages", type=str, default=None, help="Path to passages (.tsv file)")
parser.add_argument("--passages_embeddings", type=str, default=None, help="Glob path to encoded passages")
parser.add_argument(
    "--output_dir", type=str, default=None, help="Results are written to outputdir with data suffix"
)
parser.add_argument("--n_docs", type=int, default=3, help="Number of documents to retrieve per questions")
parser.add_argument(
    "--validation_workers", type=int, default=32, help="Number of parallel processes to validate results"
)
parser.add_argument("--per_gpu_batch_size", type=int, default=64, help="Batch size for question encoding")
parser.add_argument(
    "--save_or_load_index", action="store_true", help="If enabled, save index and load index if it exists"
)
parser.add_argument(
    "--model_name_or_path", type=str, help="path to directory containing model weights and config file"
)
parser.add_argument("--no_fp16", action="store_true", help="inference in fp32")
parser.add_argument("--question_maxlength", type=int, default=512, help="Maximum number of tokens in a question")
parser.add_argument(
    "--indexing_batch_size", type=int, default=1000000, help="Batch size of the number of passages indexed"
)
parser.add_argument("--projection_size", type=int, default=768)
parser.add_argument(
    "--n_subquantizers",
    type=int,
    default=0,
    help="Number of subquantizer used for vector quantization, if 0 flat index is used",
)
parser.add_argument("--n_bits", type=int, default=8, help="Number of bits per subquantizer")
parser.add_argument("--lang", nargs="+")
parser.add_argument("--dataset", type=str, default="none")
parser.add_argument("--lowercase", action="store_true", help="lowercase text before encoding")
parser.add_argument("--normalize_text", action="store_true", help="normalize text")

args = parser.parse_args()
#src.slurm.init_distributed_mode(args)
from robowaiter.utils.basic import get_root_path
retrieval_lm_path = f'{get_root_path()}/robowaiter/algos/retrieval/retrieval_lm'
args.model_name_or_path = f"{retrieval_lm_path}/../contriever-msmarco"
args.passages_embeddings = f'{retrieval_lm_path}/robot_embeddings/*'
args.no_fp16 = True
args.passages = f"{retrieval_lm_path}/fix_questions.jsonl"

class Retrieval():

    def __init__(self, threshold):
        print(f"Loading model from: {args.model_name_or_path}")
        model, tokenizer, _ = src.contriever.load_retriever(args.model_name_or_path)
        model.eval()
        #model = model.cuda()
        if not args.no_fp16:
            model = model.half()
        self.model = model
        self.tokenizer = tokenizer
        self.threshold = threshold
        index = src.index.Indexer(args.projection_size, args.n_subquantizers, args.n_bits)
        self.index = index

        # index all passages
        input_paths = glob.glob(args.passages_embeddings)
        input_paths = sorted(input_paths)
        embeddings_dir = os.path.dirname(input_paths[0])
        index_path = os.path.join(embeddings_dir, "index.faiss")
        if args.save_or_load_index and os.path.exists(index_path):
            index.deserialize_from(embeddings_dir)
        else:
            print(f"Indexing passages from files {input_paths}")
            start_time_indexing = time.time()
            index_encoded_data(index, input_paths, args.indexing_batch_size)
            print(f"Indexing time: {time.time()-start_time_indexing:.1f} s.")
            if args.save_or_load_index:
                index.serialize(embeddings_dir)

        # load passages
        passages = src.data.load_passages(args.passages)
        passage_id_map = {x["id"]: x for x in passages}
        self.passage_id_map = passage_id_map

    def get_result(self, queries):
        questions_embedding = embed_queries(args, [queries], self.model, self.tokenizer)
        top_ids_and_scores = self.index.search_knn(questions_embedding, args.n_docs)
        print(top_ids_and_scores)
        data = [{"question":queries}]
        add_passages(data, self.passage_id_map, top_ids_and_scores)

        if float(data[0]["ctxs"][0]["score"]) >= self.threshold:
            result_dict = eval(data[0]["ctxs"][0]["text"])
            result_dict["question"] = queries
            return result_dict
        else:
            return None
        # data_paths = glob.glob(args.data)
        # alldata = []
        # for path in data_paths:
        #     data = load_data(path)
        #     output_path = os.path.join(args.output_dir, os.path.basename(path))
        #
        #     queries = [ex["question"] for ex in data]
        #
        #     # get top k results
        #     start_time_retrieval = time.time()
        #     print(f"Search time: {time.time()-start_time_retrieval:.1f} s.")
        #
        #     add_passages(data, passage_id_map, top_ids_and_scores)
        #     #hasanswer = validate(data, args.validation_workers)
        #     #add_hasanswer(data, hasanswer)
        #     os.makedirs(os.path.dirname(output_path), exist_ok=True)
        #     with open(output_path, "w",encoding='utf-8') as fout:
        #         for ex in data:
        #             json.dump(ex, fout, ensure_ascii=False)
        #             fout.write("\n")
        #     print(f"Saved results to {output_path}")

if __name__ == '__main__':
    r = Retrieval(1.8)
    print(r.get_result("来一号桌"))
    print(r.get_result("去二号桌"))
    print(r.get_result("去三号桌"))
