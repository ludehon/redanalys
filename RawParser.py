import re
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


to_avoid = ["submission", "moderators"]
chars_to_remove = ["\n"]


def read_json_file(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    return json.loads(data)


def save_json_to_file(json_obj, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(json_obj, file, separators=(",", ":"), ensure_ascii=False)
        print(f'JSON object saved to {filename} successfully.')
    except Exception as e:
        print(f'Error: {e}')


"""
Return str without charaters from string list chars_to_remove
"""
def clean_str(str, chars_to_remove):
    for char in chars_to_remove:
        str = str.replace(char, " ")
    url_pattern = r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*'
    cleaned_string = re.sub(url_pattern, ' ', str)
    return cleaned_string


"""
Return true if string does not contain any element from the string list elements
"""
def contains_element(string, elements):
    return any(element in string for element in elements)


class RawParser:
    def __init__(self):
        pass

    """
    Extract the necessary information and create the new structure
    """
    def transform_json(self, input):
        output = {
            "date": input["date"],
            "subList": input["subList"],
            "data": defaultdict(dict)
        }
        for sub, posts in input["data"].items():
            print(sub)
            for post_id, post in posts.items():
                if (len(post["comments"].values()) > 0):
                    comments = [comment["body"].lower() if not contains_element(comment["body"].lower(), to_avoid) else "" for comment in post["comments"].values()]
                    post_content = post["title"] + " >> " + ".. ".join(comments)
                    output["data"][post_id] = clean_str(post_content, chars_to_remove)
        return output


"""
arg1: input file
"""
if __name__ == "__main__":
    print(f"Launched on {datetime.now().strftime('%y%m%dT%H%M%S')} with args={sys.argv}")
    rp = RawParser()
    json_in = read_json_file(sys.argv[1])
    json_out = rp.transform_json(json_in)
    save_json_to_file(json_out, f"parsed_{sys.argv[1]}")
