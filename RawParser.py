import re
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from utils import setup_logging, setup_logging
from collections import defaultdict


to_avoid = ["submission", "moderators"]
chars_to_remove = ["\n"]


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
    if (len(sys.argv) != 2):
        print(f"USAGE: python RawParser.py yyMMdd.json"); sys.exit()
    print(f"Launched on {datetime.now().strftime('%y%m%dT%H%M%S')} with args={sys.argv}")
    rp = RawParser()
    json_in = read_json_file(sys.argv[1])
    json_out = rp.transform_json(json_in)
    save_json_to_file(json_out, f"parsed_{sys.argv[1]}")
