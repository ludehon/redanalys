# REDANALYSIS
Saves reddit posts into json.
Requires a Reddit developper access.

## Launch
python3 RedditReader.py credentials_path saves_path post_limit
ex: python3 RedditReader.py /home/foobar/credentials.json /home/foobar/saves 10

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
                    "789hij": {
                        "id": "789hij",
                        "body": "comment_text",
                        "created_utc": 1693717144.0
                    }
                }
            }
        }
    }
}
