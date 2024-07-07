import json
import re

import orjson


def clean_split(text: str, seps: str, verbose: bool = False):
    """Split string, strip and clean empty part
    
    text (str): string to split
    sep (str): separator"""

    if verbose is True:
        print(seps, re.split(seps, text))

    for part in re.split(seps, text):
        if (item := part.strip()):
            yield item


def load_json(file_path) -> list | dict:
    with open(file_path, 'r', encoding='utf-8') as fr:
        return orjson.loads(fr.read())


def load_text(file_path, is_list: bool = False):
    with open(file_path, 'r', encoding='utf-8') as fr:
        fr_read = fr.read().strip()
        
    if is_list is True:
        return clean_split(fr_read, '\n')
    else:
        return fr_read
    

def write_json(data, file_path, indent=2):
    with open(file_path, 'w', encoding='utf-8', errors='surrogateescape') as fw:
        json.dump(data, fw, indent=indent, ensure_ascii=False)


def write_text(data, file_path):
    with open(file_path, 'w', encoding='utf-8', errors='surrogateescape') as fw:
        if isinstance(data, str):
            fw.write(data.strip())
        else:
            for item in data:
                fw.write(f'{item}\n')