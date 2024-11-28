import praw
import pandas as pd
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Reddit API credentials
reddit = praw.Reddit(
    client_id='Here',
    client_secret='Here',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'#user agent optional
)


def fetch_comments_from_post(post_url, limit=1000):
    """Fetch top comments from a specified Reddit post."""
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()[:limit]

    data = []
    for comment in comments:
        data.append({
            'comment_id': comment.id,
            'comment_body': comment.body,
            'comment_score': comment.score,
            'comment_created_utc': comment.created_utc,
            'comment_author': str(comment.author),
            'parent_id': comment.parent_id,
            'submission_id': comment.link_id
        })

    return data


def save_comments_to_csv(comments, filename):
    """Save the list of comments to a CSV file."""
    df = pd.DataFrame(comments)
    df['comment_created_utc'] = pd.to_datetime(
        df['comment_created_utc'], unit='s')
    df.to_csv(filename, index=False)
    logging.info(f"Saved {len(comments)} comments to {filename}.")


def main():
    post_url = 'https://www.reddit.com/r/Entrepreneur/comments/pmm6ov/i_run_an_actual_digital_marketing_agency/'
    output_file = r"C:\Users\lenovo\Desktop\reddit_top_comments.csv"

    logging.info("Starting to fetch comments...")
    comments = fetch_comments_from_post(post_url, limit=1000)
    logging.info(f"Fetched {len(comments)} comments.")

    if comments:
        save_comments_to_csv(comments, output_file)


if __name__ == "__main__":
    main()
