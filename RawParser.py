import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def read_json_file(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    return json.loads(data)


def append_post_to_file(file_name, s1, s2):
    try:
        with open(file_name, 'a') as file:
            file.write("author:\n")
            file.write(s1 + '\n')
            file.write("comments:\n")
            file.write(s2 + '\n')
            file.write("------\n")
    except Exception as e:
        print(f"Error: {e}")


class RawParser:
    def __init__(self):
        pass

    def parse_posts_and_write(self, raw_file_path, parsed_file_path):
        raw_data = read_json_file(raw_file_path)
        subs = set(raw_data["subList"])
        data = raw_data["data"]
        for sub_name in subs:
            print(f"parsing sub {sub_name}")
            posts = data[sub_name]
            for post_id, post in posts.items():
                print(f"post {post_id}")
                post_text = post["selftext"]
                comments_list = []
                for comment_id, comment in post["comments"].items():
                    comments_list.append(comment["body"])
                append_post_to_file(parsed_file_path, post_text, ". ".join(comments_list))



if __name__ == "__main__":
    print(f"Launched on {datetime.now().strftime('%y%m%dT%H%M%S')} with args={sys.argv}")
    rp = RawParser()
    parsed_data = rp.parse_posts_and_write(sys.argv[1], f"{sys.argv[1]}_parsed.txt")