import time
import facebook_scraper as fs
import pymongo
from gender_guesser import detector as gender
from datetime import datetime

MAX_COMMENTS = True

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
posts_collection = db["postids_Zitouna"]
comments_collection = db["comments_Zitouna"]

cookies = {
    'c_user': '61556291402060',
    'datr': 'b8EJZlZBuREOSfUR_pfeUcpZ',
    'dpr': '1.25',
    'fr': '1gafU3Sm8RfMhvBiS.AWWrpou6TT3sLdnVc4dxCbzHKsc.BmCzdn..AAA.0.0.BmCzdn.AWWjrgB97Ls',
    'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1712011117474%2C%22v%22%3A1%7D',
    'ps_l': '0',
    'ps_n': '0',
    'sb': 'zyvjZWq2uetDBrd-MeEXN_TW',
    'usida': 'eyJ2ZXIiOjEsImlkIjoiQXNiOXM1enN3Mjh0NSIsInRpbWUiOjE3MTE5ODUxMTF9',
    'wd': '150x728',
    'xs': '3%3A3aRWgHDOLnnXAA%3A2%3A1711915374%3A-1%3A16024%3A%3AAcXPClpSo5xJ_VKE8bZr5Am8W-f6glb7ZYaLeu1zew'
}


def save_comments(comments):
    try:
        comments_collection.insert_many(comments)
    except Exception as e:
        print(f"Error saving comments to MongoDB: {e}")

post_ids = [doc['post_id'] for doc in posts_collection.find()]
batch_size = 1000

last_successful_post_id = None
consecutive_failures = 0
resume_scraping = False

successful_posts = 0

for i in range(0, len(post_ids), batch_size):
    if resume_scraping:
        start_index = post_ids.index(last_successful_post_id)
        batch_post_ids = post_ids[start_index:start_index + batch_size]
    else:
        batch_post_ids = post_ids[i:i + batch_size]

    print(f"Scraping comments for batch {i // batch_size + 1} of size {len(batch_post_ids)}...")

    comments_list = []

    for post_id in batch_post_ids:
        print(f"Scraping comments for post {post_id}...")
        gen = fs.get_posts(
            post_urls=[post_id],
            options={"comments": MAX_COMMENTS, "progress": True},
            cookies=cookies
        )

        try:
            post = next(gen)
        except StopIteration:
            print(f"No posts found for post ID: {post_id}")
            consecutive_failures += 1
            if consecutive_failures >= 10:
                print("Stopping scraping. Too many consecutive posts with no comments.")
                resume_scraping = False
                break
            continue

        if 'comments_full' not in post:
            print(f"No comments found for post with ID: {post_id}")
            last_successful_post_id = post_id
            consecutive_failures += 1
            if consecutive_failures >= 10:
                print("Stopping scraping. Too many consecutive posts with no comments.")
                resume_scraping = False
                break
            continue

        post_caption = post.get('post_text', '')
        post_time = post.get('time', '')

        comments = post['comments_full']

        for comment in comments:
            commenter_name = comment['commenter_name']
            comment_text = comment['comment_text']
            gender_detector = gender.Detector()
            gender_result = gender_detector.get_gender(commenter_name.split(' ')[0])
            comments_list.append(
                {'bank_name': 'Banque Zitouna', 'post_id': post_id, 'post_caption': post_caption,
                 'post_time': post_time,
                 'commenter_name': commenter_name, 'gender': gender_result, 'comment_text': comment_text,
                 'scraped_time': datetime.now(datetime.UTC)})

        successful_posts += 1
        consecutive_failures = 0

    if len(comments_list) > 0:
        save_comments(comments_list)

    if resume_scraping:
        print(f"Waiting for 15 minutes before scraping the next batch...")
        time.sleep(900)
    else:
        break

print(f"Successfully scraped {successful_posts} posts.")