import os

with open(os.path.join('./goal_states_with_description.txt'), 'r', encoding='utf-8') as file:
    lines = file.readlines()

with open(os.path.join('./goal_states_with_description.jsonl'), 'w', encoding='utf-8') as file:

    for line in lines:
        tmp = line[:-1].split('\t')
        file.write("""{"title":"%s","text":"%s"}\n""" % (tmp[1], tmp[0]))
