import json
import jsonlines
import argparse


def train(args):
    # clear jsonl file
    with open("train_robot.jsonl", "a") as file_jsonl:
        file_jsonl.truncate(0)

    filename = args.passages
    with open(filename, 'r', encoding="utf-8") as f:
        k = 0
        for line in f:
            data = json.loads(line)
            dict = {"id": k, 'title': data['title'], 'text': data['text']}
            k += 1
            with jsonlines.open("train_robot.jsonl", "a") as file_jsonl:
                file_jsonl.write(dict)


def test(args):
    # clear
    with open("test_robot.jsonl", "a") as file_jsonl:
        file_jsonl.truncate(0)

    filename = args.passages
    with open(filename, 'r', encoding="utf-8") as f:
        # k=0
        for line in f:
            # if k<1000:
            data = json.loads(line)
            dict = {"id": data['id'], 'question': data['title'], 'answers': data['text']}
            # k+=1
            with jsonlines.open("test_robot.jsonl", "a") as file_jsonl:
                file_jsonl.write(dict)


def test(args):
    # clear
    with open("test_robot.jsonl", "a") as file_jsonl:
        file_jsonl.truncate(0)

    filename = args.passages
    with open(filename, 'r', encoding="utf-8") as f:
        k = 0
        for line in f:
            # if k<1000:
            data = json.loads(line)
            dict = {"id": k, 'question': data['title']}
            k += 1
            with jsonlines.open("test_robot.jsonl", "a") as file_jsonl:
                file_jsonl.write(dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--passages", type=str, default=None, help="Path to passages")
    parser.add_argument("--mode", type=str, default=None, help="train or llm_test")

    args = parser.parse_args()

    if args.mode == 'train':
        train(args)
    elif args.mode == 'llm_test':
        test(args)
    else:
        print("error mode!")
