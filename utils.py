import json
import logging
from datetime import datetime

def setup_logging():
    log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M.log")
    logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json_file(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    return json.loads(data)


def save_json_to_file(json_obj, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(json_obj, file, separators=(",", ":"), ensure_ascii=False)
        logging.info(f'JSON object saved to {filename} successfully.')
    except Exception as e:
        logging.error(f'Error: {e}')
