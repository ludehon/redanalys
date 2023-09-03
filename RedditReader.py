import sys
import praw
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict



def read_json_file(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    return json.loads(data)

def save_json_to_file(json_obj, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(json_obj, file, separators=(",", ":"))
        print(f'JSON object saved to {filename} successfully.')
    except Exception as e:
        print(f'Error: {e}')

def merge_complex_dicts(dict1, dict2):
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged:
            if isinstance(value, dict) and isinstance(merged[key], dict):
                merged[key] = merge_complex_dicts(merged[key], value)
            elif isinstance(value, list) and isinstance(merged[key], list):
                for item in value:
                    if item not in merged[key]:
                        merged[key].append(item)
            else:
                merged[key] = value
        else:
            merged[key] = value
    return merged


class RedditReader:
    def __init__(self, credentials_fileName):
        credentials = read_json_file(credentials_fileName)
        self.reddit = praw.Reddit(
            client_id = credentials.get("client_id"),
            client_secret = credentials.get("client_secret"),
            user_agent = credentials.get("user_agent"),
        )

    def get_comments_from_subreddit(self, subreddits, post_limit=1000):
        # root level
        all_posts = {
            "date": datetime.now().strftime("%y%m%d"),
            "subList": subreddits,
            "data": defaultdict(dict)
        }
        # data level
        for subreddit_name in subreddits:
            print(f"processing subreddit: {subreddit_name}")
            subreddit = self.reddit.subreddit(subreddit_name)
            post_list = list(subreddit.new(limit=post_limit))

            posts_json = {}
            # post level
            for post_number, post in enumerate(post_list):
                if (datetime.utcfromtimestamp(post.created_utc).date() != datetime.utcnow().date()):
                    continue
                post_dict = {
                    "id": post.id,
                    "title": post.title,
                    "author": post.author.name if post.author else None,
                    "created_utc": post.created_utc,
                    "score": post.score,
                    "upvote_ratio": post.upvote_ratio,
                    "url": post.url,
                    "selftext": post.selftext,
                    "comments": {}
                }
                # comments level
                for comment_number, comment in enumerate(post.comments.list()[:]):
                    if not isinstance(comment, praw.models.MoreComments):
                        # print(f"    {comment_number}/{len(post.comments.list())-1}")
                        comment_dict = {
                            "id": comment.id,
                            "author": comment.author.name if comment.author else None,
                            "body": comment.body if comment.body else None,
                            "created_utc": comment.created_utc if comment.created_utc else None,
                            "score": comment.score if comment.score else None
                        }
                        post_dict["comments"][comment.id] = comment_dict
                # adding all posts to the sub dic
                all_posts["data"][subreddit_name][post.id] = post_dict
        return all_posts

    def save_comments(self):
        pass

"""
arg1: credentials
arg2: saves path
arg3: post limit
"""
if __name__ == "__main__":
    print(f"Launched on {datetime.now().strftime('%y%m%dT%H%M%S')} with args={sys.argv}")
    rr = RedditReader(sys.argv[1])
    all_posts = rr.get_comments_from_subreddit(["stocks", "wallstreetbets", "investing", "stockmarket"], int(sys.argv[3]))
    file_path = Path(all_posts["date"])
    if file_path.exists():
        print(f"merging data from {all_posts['date']}")
        existing_data = read_json_file(file_path)
        updated_data = merge_complex_dicts(existing_data, all_posts)
        save_json_to_file(updated_data, f"{sys.argv[2]}/{updated_data['date']}.json")
        print(f"data from {all_posts['date']} merged successfully")
    else:
        print(f"saving data from {all_posts['date']}")
        save_json_to_file(all_posts, f"{sys.argv[2]}/{all_posts['date']}.json")
        print(f"data from {all_posts['date']} saved successfully")