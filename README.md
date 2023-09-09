# REDANALYSIS
## Features
- Saves reddit posts into json
- Parse and clean posts/comments
- Summarize posts/comments

## Requirements
- Reddit developper access
- OogaBooga API access
Informations must be filled into a json credentials file, format :
{
    "client_id":"",
    "client_secret":"",
    "user_agent":"",
    "host": "",
    "subreddits": ["", ""]
}

## Usage
python3 RedditReader.py credentials_path saves_path post_limit


## Saves format:
{
    "date": "230903",
    "subList": [
        "sub1",
        "sub2"
    ],
    "data": {
        "sub1": {
            "123abc": {
                "id": "123abc",
                "title": "post_title",
                "created_utc": 1693717143.0,
                "selftext": "post_text",
                "comments": {
                    "dddddd": {
                        "id": "dddddd",
                        "body": "comment_text",
                        "created_utc": 1693717144.0
                    },
                    "eeeeee": {
                        "id": "eeeeee",
                        "body": "comment_text",
                        "created_utc": 1693717144.0
                    }
                }
            }
        }
    }
}

## Parsed format:
{
    "date": "230903",
    "subList": [
        "sub1",
        "sub2"
    ],
    "data": {
        "123abc": "parsed post and comments"
    }
}

## Summarized format:
same as parsed format