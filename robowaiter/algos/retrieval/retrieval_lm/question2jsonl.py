import time

import openai
from colorama import init, Fore
from loguru import logger
from robowaiter.llm_client.tool_register import get_tools, dispatch_tool
import requests
import json
from collections import deque
import re
import jsonlines


def question2jsonl(file_path, output_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        lines = f.read().strip()

    sections = re.split(r'\n\s*\n', lines)
    with jsonlines.open(output_path, "w") as file_jsonl:
        k = 0

        for s in sections:
            x = s.strip().splitlines()
            if len(x) == 2:
                answer_dict = {
                    "answer": x[1],
                    "function": None
                }
            else:
                answer_dict = {
                    "answer": x[1],
                    "function": x[2],
                    "args": x[3]
                }

            item_dict = {"id": k, 'title': x[0], 'text': str(answer_dict)}
            file_jsonl.write(item_dict)
            k += 1

def question2jsonl_test(file_path, output_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        lines = f.read().strip()

    sections = re.split(r'\n\s*\n', lines)
    with jsonlines.open(output_path, "w") as file_jsonl:
        k = 0

        for s in sections:
            x = s.strip().splitlines()

            item_dict = {"id": k, 'question': x[0]}
            file_jsonl.write(item_dict)
            k += 1


if __name__ == '__main__':
    file_path = "fix_questions.txt"
    output_path = "fix_questions.jsonl"
    question2jsonl(file_path,output_path)