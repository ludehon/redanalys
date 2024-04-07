import os
import sys
import logging
from datetime import datetime
from utils import setup_logging, setup_logging
from Summarizer import Summarizer
from RawParser import RawParser
from utils import read_json_file, save_json_to_file

setup_logging()

# Find the filenames that are in folder1 but not in folder2
def compare_folders(folder1, folder2):
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)
    filenames1 = {filename.split('.')[0] for filename in files1 if not filename.startswith('.')}
    filenames2 = {filename.split('.')[0] for filename in files2 if not filename.startswith('.')}
    difference = filenames1 - filenames2
    return [filename + '.json' for filename in difference]


if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print(f"USAGE: python Workflow.py credentials.json folder_path mode=['parse', 'sum', 'both']"); sys.exit()
    logging.info(f"Launched on {datetime.now().strftime('%y%m%dT%H%M%S')} with args={sys.argv}")

    credentials = read_json_file(sys.argv[1])
    folder_path = sys.argv[2]
    mode = sys.argv[3]

    if (mode in ["parse", "both"]):
        # Parse raw data
        rp = RawParser()
        to_parse = compare_folders(f"{folder_path}/raw", f"{folder_path}/parsed")
        for filename in to_parse:
            json_in = read_json_file(f"{folder_path}/raw/{filename}")
            json_out = rp.transform_json(json_in)
            save_json_to_file(json_out, f"{folder_path}/parsed/{filename}")

    if (mode in ["sum", "both"]):
        # Summarize parsed data
        seed = 759718164
        instruction = "Here are messages exchanged by different persons, write a very short summary in 3 bullet points, keeping only the most important and relevant details:"
        su = Summarizer(credentials["host"], instruction, seed)

        to_sum = compare_folders(f"{folder_path}/parsed", f"{folder_path}/summed")
        logging.info(f"Files to summarize : {len(to_sum)}")
        for filename in to_sum:
            logging.info(f"summarizing file {filename}")
            input = read_json_file(f"{folder_path}/parsed/{filename}")
            summary = su.summarize_json(input)
            save_json_to_file(summary, f"{folder_path}/summed/{filename}")
