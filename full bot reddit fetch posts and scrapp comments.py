import praw
import pandas as pd
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reddit API credentials
reddit = praw.Reddit(
    client_id='YOUR ID',
    client_secret='YOUR CS',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    #your user agent
)

def search_and_fetch_posts(keyword, subreddits, limit=1000):
    """Search for posts containing the keyword across specified subreddits."""
    posts = reddit.subreddit('+'.join(subreddits)).search(keyword, limit=limit)
    data = []

    for post in posts:
        data.append({
            'post_id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'author': str(post.author),
            'subreddit': post.subreddit.display_name,
            'url': post.url
        })

    return data

def fetch_comments_from_post(post_url, limit=100):
    """Fetch top comments from a specified Reddit post."""
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()[:limit]

    comment_data = []
    for comment in comments:
        comment_data.append({
            'comment_id': comment.id,
            'comment_body': comment.body,
            'comment_score': comment.score,
            'comment_created_utc': comment.created_utc,
            'comment_author': str(comment.author),
            'parent_id': comment.parent_id,
            'submission_id': comment.link_id
        })

    return comment_data

def save_posts_and_comments_to_excel(posts, filename):
    """Save the list of posts and their comments to an Excel file."""
    all_data = []
    for post in posts:
        comments = fetch_comments_from_post(post['url'], limit=100)  # Fetch up to 100 top comments per post
        for comment in comments:
            data_row = {**post, **comment}
            all_data.append(data_row)
    
    df = pd.DataFrame(all_data)
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    df['comment_created_utc'] = pd.to_datetime(df['comment_created_utc'], unit='s')
    df.to_excel(filename, index=False, engine='openpyxl')
    logging.info(f"Saved {len(all_data)} rows (posts + comments) to {filename}.")

# Ocrevus, Briumvi, Kesimpta, Tysabri, ms , and, but, MultipleSclerosis ,treatment ,Exercise
def main():
    keyword = 'ms'
    subreddits = ['MultipleSclerosis']
    output_file = r"C:\Users\lenovo\Desktop\pphadddddreiiddit_posts_and_comments015.xlsx"
    
    logging.info("Starting to search posts...")
    posts = search_and_fetch_posts(keyword, subreddits, limit=10)
    logging.info(f"Fetched a total of {len(posts)} posts.")
    
    if posts:
        save_posts_and_comments_to_excel(posts, output_file)

if __name__ == "__main__":
    main()
