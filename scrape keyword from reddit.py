import praw
import pandas as pd
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reddit API credentials
reddit = praw.Reddit(
    client_id='Here',
    client_secret='Here',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
)

def search_and_fetch_posts(keyword, subreddits, limit=1000):
    """Search for posts containing the keyword across specified subreddits."""
    posts = reddit.subreddit('+'.join(subreddits)).search(keyword, limit=limit)
    data = []

    for post in posts:
        data.append({
            'post_id': post.id,
            'title': post.title,
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'author': str(post.author),
            'subreddit': post.subreddit.display_name,
            'url': post.url
        })

    return data

def save_posts_to_excel(posts, filename):
    """Save the list of posts to an Excel file."""
    df = pd.DataFrame(posts)
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    df.to_excel(filename, index=False, engine='openpyxl')
    logging.info(f"Saved {len(posts)} posts to {filename}.")

    #]
def main():
    keyword = 'digital marketing'
    subreddits = ['Entrepreneur']
    output_file = r"C:\Users\lenovo\Desktop\mortgage_postsinf025.xlsx"
    
    logging.info("Starting to search posts...")
    posts = search_and_fetch_posts(keyword, subreddits, limit=1000)
    logging.info(f"Fetched a total of {len(posts)} posts.")
    
    if posts:
        save_posts_to_excel(posts, output_file)

if __name__ == "__main__":
    main()
