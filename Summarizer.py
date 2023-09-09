import sys
import json
import html
import requests
from datetime import datetime
from collections import defaultdict


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


class Summarizer:
    def __init__(self, host, instruction, seed):
        self.host = host
        self.uri = f'http://{self.host}/api/v1/chat'
        self.instruction = instruction
        self.history = {'internal': [], 'visible': []}
        self.seed = seed

    def run(self, user_input, history):
        request = {
            'user_input': user_input,
            'max_new_tokens': 250,
            'auto_max_new_tokens': False,
            'max_tokens_second': 0,
            'history': history,
            'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'Example',
            'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
            'your_name': 'You',
            # 'name1': 'name of user', # Optional
            # 'name2': 'name of character', # Optional
            # 'context': 'character context', # Optional
            # 'greeting': 'greeting', # Optional
            # 'name1_instruct': 'You', # Optional
            # 'name2_instruct': 'Assistant', # Optional
            # 'context_instruct': 'context_instruct', # Optional
            # 'turn_template': 'turn_template', # Optional
            'regenerate': False,
            '_continue': False,
            'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            'preset': 'None',
            'do_sample': True,
            'temperature': 0.1,
            'top_p': 0.1,
            'typical_p': 1,
            'epsilon_cutoff': 0,  # In units of 1e-4
            'eta_cutoff': 0,  # In units of 1e-4
            'tfs': 1,
            'top_a': 0,
            'repetition_penalty': 1.18,
            'repetition_penalty_range': 0,
            'top_k': 40,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,
            'guidance_scale': 1,
            'negative_prompt': '',
            'seed': self.seed,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': []
        }

        response = requests.post(self.uri, json=request)
        if response.status_code == 200:
            result = response.json()['results'][0]['history']
            return html.unescape(result['visible'][-1][1])

    def summarize(self, json):
        output = {
            "date": input["date"],
            "subList": input["subList"],
            "data": defaultdict(dict)
        }
        i = 0
        for post_id, post_text in json["data"].items():
            i = i + 1
            print(f"processing {i} on {len(json['data'].values())}")
            output["data"][post_id] = self.run(f"{self.instruction} {post_text}", self.history)
        return output


"""
arg1: credentials file
arg2: json to summarize
"""
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"USAGE: python Summarizer.py credentials.json parsed_yyMMdd.json"); sys.exit()
    print(f"Launched on {datetime.now().strftime('%y%m%dT%H%M%S')} with args={sys.argv}")

    credentials = read_json_file(sys.argv[1])
    seed = 759718164
    instruction = "Here are messages exchanged by different persons, you should write a very short summary in 3 bullet points, highlighting the important subject:"
    su = Summarizer(credentials["host"], instruction, seed)

    input = read_json_file(sys.argv[2])
    summary = su.summarize(input)
    save_json_to_file(summary, f"summed_{sys.argv[2]}")
