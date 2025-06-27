import praw
import time
from envparse import env

import matcher
import filters
import json

def markdownFormatForCard(card):
    # shown:   CARD_NAME (SET, #)
    # link to:  image   full_details
    return f'[{card["cardName"]}]({card["cardImageURL"]}) ([{card["setName"]}, {card["cardNumber"]}]({card["cardURL"]}))'

def main():
    client_id = env("REDDIT_CLIENT_ID")
    client_secret = env("REDDIT_CLIENT_SECRET")
    username = env("REDDIT_USERNAME")
    password = env("REDDIT_PASSWORD")
    user_agent = env("REDDIT_USER_AGENT", default="test bot by /u/toastyoven13")
    
    # Authenticate with Reddit
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    # target subreddit
    subreddit = reddit.subreddit('test_posts')

    cardList = []
    with open("data/cardList.json", "r", encoding="utf_16") as f:
         cardList = json.load(f)

    # only look at promo or diamond cards
    cardList = list(filter(lambda x: filters.DiamondRarity()(x) or filters.Promo()(x), cardList))

    print("Bot is running...")
    # TODO: listen to comments too
    for post in subreddit.stream.submissions():
        try:
            # Only post on my submissions
            if 'toastyoven13' == post.author:
                print(f"Found a post by toastyoven13: {post.title}")
                results = []
                matches = matcher.GetMatches(post.selftext)
                if len(matches) == 0:
                    continue
                for m in matches:
                    cards = filter(filters.ByName(m.strip(" ")), cardList)
                    # TODO: apply multiple filters
                    results.append(list(cards))

                # assemble the reddit markdown post
                markdown = ""
                for r in results:
                    if len(r) == 0:
                        continue
                    markdown += "-"
                    for card in r:
                        markdown += f' {markdownFormatForCard(card)}'
                    markdown += "\n"

                print(markdown)  # TODO: remove
                if markdown != "":
                    post.reply(markdown)
                    print("Replied to the comment")
                else:
                    print("Did not reply to the comment")
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(30) # Wait before retrying in case of an error

if __name__ == "__main__":
    main()