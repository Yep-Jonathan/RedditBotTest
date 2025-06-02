import praw
import time
from envparse import env

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

    print("Bot is running...")
    for post in subreddit.stream.submissions():
        print(f"title: {post.title}, author: {post.author}")
        try:
            # Check if the comment contains a specific keyword
            if 'toastyoven13' == post.author:
                print(f"Found a post by toastyoven13: {post.title}")
                # Reply to the comment
                post.reply("Another automated reply: Thank you for your post!")
                print("Replied to the comment.")
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(30) # Wait before retrying in case of an error

if __name__ == "__main__":
    main()