# This file is used to count benchmark data under different tasks and datasets, and other useful statistics.
import json
import os
tasks = ['EAE','ED','NER','RE']
test_file_name = 'test-prompt.json'
for task in tasks:
    data_set_path = os.path.join('SFT_data/benchmark', task, test_file_name)
    with open(data_set_path, 'r') as f:
        lines = f.readlines()
        data = json.loads(lines[0])
        for k,v in data.items():
            print(f'{task} {k} {v}')
    


