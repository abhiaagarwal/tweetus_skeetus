import os
from datetime import datetime

import atprototools as atp  # https://github.com/ianklatzco/atprototools/tree/master
from dotenv import load_dotenv
from twitter.scraper import Scraper  # twitter-api-client


def tweetus_skeetus() -> None:
    BSKY_USERNAME = os.environ.get("BSKY_USERNAME")
    assert BSKY_USERNAME is not None
    BSKY_PASSWORD = os.environ.get("BSKY_PASSWORD")
    assert BSKY_PASSWORD is not None
    bsky_session = atp.Session(BSKY_USERNAME, BSKY_PASSWORD)

    TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
    assert TWITTER_EMAIL is not None
    TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
    assert TWITTER_USERNAME is not None
    TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")
    assert TWITTER_PASSWORD is not None
    TWITTER_ID = os.environ.get("TWITTER_ID")
    assert TWITTER_ID is not None
    TWITTER_ID = int(TWITTER_ID)

    DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"

    scraper = Scraper(TWITTER_EMAIL, TWITTER_USERNAME, TWITTER_PASSWORD)
    tweets = scraper.tweets([TWITTER_ID], limit=1)[0][0]["data"]["user"]["result"][
        "timeline_v2"
    ]["timeline"]["instructions"][1]["entries"]
    for tweet in tweets:
        try:
            tweet_content = tweet["content"]["itemContent"]["tweet_results"]["result"][
                "legacy"
            ]
            text = tweet_content["full_text"]
            created_at = datetime.strptime(tweet_content["created_at"], DATE_FORMAT)
            bsky_session.post_bloot(
                postcontent=text, image_path=None, timestamp=created_at
            )
        except KeyError:
            # I do not care why this is happening, just skip it
            continue


if __name__ == "__main__":
    load_dotenv()
    tweetus_skeetus()
