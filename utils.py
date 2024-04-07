import json
import logging
from datetime import datetime


def setup_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M.log")
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console (stream) handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

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
