import asyncio
from envparse import env
import json
import asyncpraw
import time

import filters
import interpret
import matcher

def markdownFormatForCard(card):
    # shown:   CARD_NAME (SET, #)
    # link to:  image   full_details
    return f'[{card["cardName"]}]({card["cardImageURL"]}) ([{card["setName"]}, {card["cardNumber"]}]({card["cardURL"]}))'

class Post:
    def __init__(self, author, text, reply, submissionAuthor):
        self.author = author
        self.submissionAuthor = submissionAuthor
        self.text = text
        self.reply = reply

async def monitorAndReply(queue):
    cardList = []
    with open("data/cardList.json", "r", encoding="utf_16") as f:
         cardList = json.load(f)

    # only look at promo or diamond cards
    cardList = list(filter(lambda x: filters.DiamondRarity()(x) or filters.Promo()(x), cardList))

    while True:
        post = await queue.get()
        if post is None:
            break

        try:
            if 'toastyoven13' != post.submissionAuthor:
                # print(f"Skipping post by {post.author}")
                continue  # FIXME: Listen to all submissions; skip this bot's submissions

            print(f"Processing post by {post.author}: {post.text[:50]}...")
            results = []
            matches = matcher.Match(post.text)
            if len(matches) == 0:
                print(f"  No matches found")
                continue

            for m in matches:
                cards = interpret.Interpret(m, cardList)
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
                await post.reply(markdown)
                print("Replied to the comment")
            else:
                print("Did not reply to the comment")
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(30) # Wait before retrying in case of an error

async def monitorSubreddit(subreddit, queue):
    async def monitorSubmissions():
        async for submission in subreddit.stream.submissions(skip_existing=True):
            await queue.put(Post(submission.author, submission.selftext, submission.reply, submission.author))

    async def monitorComments():
        async for comment in subreddit.stream.comments(skip_existing=True):
            await comment.submission.load()
            await queue.put(Post(comment.author, comment.body, comment.reply, comment.submission.author))

    async with asyncio.TaskGroup() as tg:
        tg.create_task(monitorSubmissions())
        tg.create_task(monitorComments())


async def main():
    client_id = env("REDDIT_CLIENT_ID")
    client_secret = env("REDDIT_CLIENT_SECRET")
    username = env("REDDIT_USERNAME")
    password = env("REDDIT_PASSWORD")
    user_agent = env("REDDIT_USER_AGENT", default="test bot by /u/toastyoven13")

    subredditName = env("REDDIT_SUBREDDIT", default="test_posts")

    # Authenticate with Reddit
    reddit = asyncpraw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent
    )

    # TODO: Ability to listen to multiple subreddits
    # target subreddit
    subreddit = await reddit.subreddit(subredditName)

    print("Bot is running...")

    async with asyncio.TaskGroup() as tg:
        queue = asyncio.Queue(100)
        tg.create_task(monitorAndReply(queue))
        tg.create_task(monitorSubreddit(subreddit, queue))

    print("Bot finished running")

if __name__ == "__main__":
    asyncio.run(main())
