import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def read_json_file(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    return json.loads(data)


class RawParser:
    def __init__(self):
        pass

    def concatenate_fields(self, data):
        content = ""
        if "title" in data:
            content += data["title"] + " "
        if "selftext" in data:
            content += data["selftext"] + " "
        if "comments" in data:
            comments = " ".join(comment["body"] for comment in data["comments"].values())
            content += comments
        return content.strip()

    """
    Read the original JSON data from input_file
    Extract the necessary information and create the new structure
    Write the transformed JSON data to output_file
    """
    def transform_json(self, input_file, output_file):
        with open(input_file, 'r') as f:
            original_data = json.load(f)

        sub_list = original_data["subList"][0] if original_data["subList"] else None
        main_entry = next(iter(original_data["data"][sub_list].values())) if sub_list else None

        if sub_list and main_entry:
            transformed_data = {
                "date": original_data["date"],
                "subList": original_data["subList"],
                "data": {
                    sub_list: {
                        key: {
                            "content": self.concatenate_fields(value)
                        }
                        for key, value in original_data["data"][sub_list].items()
                    }
                }
            }

            with open(output_file, 'w') as f:
                json.dump(transformed_data, f, indent=4)

"""
arg1: input file
"""
if __name__ == "__main__":
    print(f"Launched on {datetime.now().strftime('%y%m%dT%H%M%S')} with args={sys.argv}")
    rp = RawParser()
    rp.transform_json(sys.argv[1], "output.json")