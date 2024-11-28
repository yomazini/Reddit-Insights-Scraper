import praw
import pandas as pd
import logging
from prawcore.exceptions import RequestException, ServerError

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reddit API credentials
reddit = praw.Reddit(
    client_id='Here',
    client_secret='Here',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'#user agent optional
) 

def fetch_subreddit_posts(subreddit_name, limit=100):
    """Fetch posts from a specified subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    
    try:
        for post in subreddit.top(limit=limit):
            posts.append({
                'id': post.id,
                'title': post.title,
                'score': post.score,
                'selftext': post.selftext,
                'url': post.url,
                'created_utc': post.created_utc,
                'num_comments': post.num_comments,
                'author': str(post.author),
                'subreddit': str(post.subreddit),
                'permalink': post.permalink
            })
        logging.info(f"Fetched {len(posts)} posts from r/{subreddit_name}.")
    except (RequestException, ServerError) as e:
        logging.error(f"Error fetching posts: {e}")
    
    return posts

def save_posts_to_csv(posts, filename):
    """Save the list of posts to a CSV file."""
    df = pd.DataFrame(posts)
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    df.to_csv(filename, index=False)
    logging.info(f"Saved {len(posts)} posts to {filename}.")

def main():
    subreddit_name = 'morocco'
    limit = 1000
    output_file = r"C:\Users\lenovo\Desktop\test01.csv"
    
    posts = fetch_subreddit_posts(subreddit_name, limit)
    if posts:
        save_posts_to_csv(posts, output_file)

if __name__ == "__main__":
    main()
