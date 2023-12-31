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
        self.uri = f'http://{self.host}/v1/chat/completions'
        self.instruction = instruction
        self.seed = seed
        self.headers = {"Content-Type": "application/json"}

    def run(self, str):
        history = [{"role": "user", "content": self.instruction + str}]
        data = {
            "messages": history,
            'mode': 'instruct',
            'temperature': 0.1,
            'max_new_tokens': 250,
            # 'auto_max_new_tokens': False,
            # 'max_tokens_second': 0,
            # 'character': 'Example',
            # 'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
            # 'your_name': 'You',
            # 'regenerate': False,
            # '_continue': False,
            # 'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',
            # 'preset': 'None',
            # 'do_sample': True,
            # 'top_p': 0.1,
            # 'typical_p': 1,
            # 'epsilon_cutoff': 0,  # In units of 1e-4
            # 'eta_cutoff': 0,  # In units of 1e-4
            # 'tfs': 1,
            # 'top_a': 0,
            # 'repetition_penalty': 1.18,
            # 'repetition_penalty_range': 0,
            # 'top_k': 40,
            # 'min_length': 0,
            # 'no_repeat_ngram_size': 0,
            # 'num_beams': 1,
            # 'penalty_alpha': 0,
            # 'length_penalty': 1,
            # 'early_stopping': False,
            # 'mirostat_mode': 0,
            # 'mirostat_tau': 5,
            # 'mirostat_eta': 0.1,
            # 'guidance_scale': 1,
            # 'negative_prompt': '',
            # 'seed': self.seed,
            # 'add_bos_token': True,
            # 'truncation_length': 2048,
            # 'ban_eos_token': False,
            # 'skip_special_tokens': True,
            # 'stopping_strings': []
        }

        response = requests.post(self.uri, headers=self.headers, json=data)
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            return result
        else:
            print(f"Error when contacting API. Code : {response.status_code}")
            print(f"{response}")
            sys.exit(1)

    def summarize_json(self, json):
        output = {
            "date": input["date"],
            "subList": input["subList"],
            "data": defaultdict(dict)
        }
        i = 0
        for post_id, post_text in json["data"].items():
            i = i + 1
            print(f"processing {i} on {len(json['data'].values())}")
            output["data"][post_id] = self.run(post_text)
        return output
    
    def summarize_string(self, str):
        output = self.run(str)
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
    summary = su.summarize_json(input)
    save_json_to_file(summary, f"summed_{sys.argv[2]}")
    # mystr = """Is anyone successfully outsourcing service based work as a middleman? >> yes, it’s called being a “general contractor”.. anyone with a successful cash flower that’s worth any effort doesn’t sell you courses on it, they go do it.   i’ve bought 3 companies, started 4, been a ceo, self built wealth.  i’d rather message a few pointers for free out of the joy it brings seeing others do well. no youtube course, lol.   helps to stop reading about “doing”, and go “do” the things….. we outsource a % of lead generation for my b2b technology sales agency.   we have a flat structure and out senior people on work, allowing us to charge a lot. then for the grinding work we hire internal juniors but also agency partners to help scale our funnel.   agency models can make a lot and without the overhead of traditional companies.   can you sell? manage clients? hire? if so, agency will crush the companies you’re helping. not even close... in service industries the pricing will be fairly commoditised so the margin will have to come from the price of acquisition. if you can get orders for less than what the actual service providers would pay to get them you can profit from the difference.  it costs my company about £25 to acquire a customer so if someone knew how to do it for £10 the could easily charge me £20 and pocket the difference.  the other option is to buy the service in bulk at a lower price and try to then effectively resell them individually at a higher price.  i would happily give you a 10% discount if you were willing to buy 20% of my capacity for the next 12 months. if you then are able to resell all of that for full price you would pocket the difference... agreed…. i’m willing to bet i’ve helped more people get their first real estate wholesale or fix and flip deal done for free than the “guru’s” have selling courses and mentorship’s …. i’ve made it myself, built my own businesses - i don’t need to be paid to help people get going, i enjoy it, especially for people who are already out there trying and just need a nudge in the right direction. i’ve helped a number of my employees get out and start their own companies even to my own detriment, helped broker deals i get nothing out of, taught people to do businesses that i’m involved in, even if they become my competition….all for the love of the game  people who are actually successful, very often give back more than anyone will ever notice.   all that said, i have bought courses that were helpful and worth the money, but most of them are too expensive up front and people are forced to spend more money than they have to figure out if it’s even something they actually want to do or not. not a good bet for most.  i’ve considered starting a coaching company teaching real estate wholesaling targeted towards a demographic with very low income but very high ambition…. like a grocery store clerk who wants to make something of themself.  i’d charge a small weekly fee (maybe $100) and 50% of their first deal, but when they get their first deal, i’d deduct whatever they’ve spent so far from the 50% going my way. say the first deal makes 12k and it took them 50 weeks of coaching to do it. that would be 6k to them and 6k to me, but since i’ve collected 5k from them over those 50 weeks, that gets deducted from the 6k coming to me and i’d only take $1,000, they keep the 11k.  i do believe putting up money is an important part of the process - weekly input means they will stay motivated and keep pushing to work harder, and see it through to the end. plus the notion of forced savings/losing the money they’ve put in if they don’t get a deal done would help through the hard times they are sure to experience along the way. i’d host group weekly coaching calls with goal setting and review, some type of individual or one on one time. and just spend a year educating and walking them through all the pieces of putting together a deal. by the end of it they’ll have the knowledge, education, experience, connections and capital to do the next deal on their own.  i did a test pilot of this idea a couple years ago, and it got some good traction and a lot of interest…. i put it down when one of my companies experienced some unexpected growth…. maybe i’ll pick this up again for 2024 🤔.. some are probably great. there are also online coaches i think are good, especially with niche professional dev.   i’m more thinking of the ones touting solopreneurial success when they’ve done nothing themselves."""
    # print(su.summarize_string(mystr))
