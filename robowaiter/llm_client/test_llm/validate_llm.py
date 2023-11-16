import os
import sys
from tqdm import tqdm

sys.path.append(os.path.join('../../llm_client'))

from tool_api import run_conversation
from tool_register import get_tools

functions = get_tools()

with open(os.path.join('./validate_data.txt'), 'r', encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line[:-1].split('\t') for line in lines]

with open(os.path.join('./validate_llm_1.txt'), 'w', encoding='utf-8') as file:
    for line in tqdm(lines):
        query = line[0]
        file.write(str(run_conversation(query=query, stream=False)) + '\n')
